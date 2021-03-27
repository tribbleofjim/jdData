import jieba.analyse
import mongo_conn
import util
from array import array
import redis
import ast
import setting


data_conn = mongo_conn.MongoConn(host=setting.mongo_params['host'],
                                 user=setting.mongo_params['user'],
                                 password=setting.mongo_params['password'],
                                 database=setting.mongo_params['database'],
                                 collection=setting.mongo_params['data_collection'])

analyze_conn = mongo_conn.MongoConn(host=setting.mongo_params['host'],
                                    user=setting.mongo_params['user'],
                                    password=setting.mongo_params['password'],
                                    database=setting.mongo_params['database'],
                                    collection=setting.mongo_params['analyze_collection'])

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

jieba.analyse.set_stop_words(setting.stopwords_path)


def jieba_test():
    sentence = ''
    with open('./text_words/jieba_test', 'r', encoding='utf-8') as file:
        for line in file.readlines():
            if line == '\n':
                line = line.strip('\n')
            sentence += line
    print(sentence)
    res = jieba.analyse.textrank(sentence, topK=10, withWeight=True)
    print(res)
    return 0


def get_item_info(sku_id):
    item = __get_item_from_redis(sku_id)
    del item['commentList']
    return item


def get_item_season_data(sku_id):
    item = __get_item_from_redis(sku_id)
    season_data = __get_item_data(item)
    categories = list()
    item_data = list()
    cate_idx = -1
    for cate, data in season_data.items():
        if cate == '' or None:
            cate = '普通版'
        if cate not in categories:
            categories.append(cate)
            cate_idx += 1
        for i in range(0, len(data)):
            item_data.append([cate_idx, i, data[i]])
    return {
        'categories': categories,
        'item_data': item_data
    }


def get_good_words(sku_id):
    item = __get_item_from_redis(sku_id)
    comments = item['commentList']
    res_comments = list()
    idx = 0
    sentence = ''
    for comment in comments:
        if comment['star'] > 3:
            sentence += comment['content']
            if idx < 5:
                comment['isPlus'] = '是' if comment['isPlus'] else '否'
                res_comments.append(comment)
                idx += 1
    words = jieba.analyse.textrank(sentence, topK=20, withWeight=True)
    return {
        'words': [{'name': x[0], 'value': round(x[1], 2) * 100} for x in words],
        'comments': res_comments
    }


def get_bad_words(sku_id):
    item = __get_item_from_redis(sku_id)
    comments = item['commentList']
    res_comments = list()
    idx = 0
    sentence = ''
    for comment in comments:
        if comment['star'] <= 3:
            sentence += comment['content']
            if idx < 5:
                comment['isPlus'] = '是' if comment['isPlus'] else '否'
                res_comments.append(comment)
                idx += 1
    words = jieba.analyse.textrank(sentence, topK=20, withWeight=True)
    return {
        'words': [{'name': x[0], 'value': round(x[1], 2) * 100} for x in words],
        'comments': res_comments
    }


def __get_item_from_redis(sku_id):
    item = r.get(sku_id)
    if item is None:
        item = data_conn.find_one(query={'skuId': sku_id}, projection={'_id': 0})
        __get_item_recom(item)
        r.set(sku_id, item)
    else:
        item = ast.literal_eval(item)
    r.expire(sku_id, 1800)
    return item


def __get_item_recom(item):
    sell_count = util.get_sell_count(item['sellCount'])
    category = item['productClass']
    if category is None:
        range_sell_count = sell_count
    else:
        first_cate = category.split('-')[0]
        sell_counts = analyze_conn.find_one(query={'first_cate': {'$regex': '^' + first_cate},
                                                   'all_sum': {'$exists': True}},
                                            projection={'_id': 0, 'sell_count': 1})['sell_count']
        bias = (sell_counts[0] - sell_counts[1]) / 3
        if (sell_count - sell_counts[1]) < sell_counts[1] + bias:
            range_sell_count = 0.33
        elif (sell_count - sell_counts[1]) < sell_counts[1] + 2 * bias:
            range_sell_count = 0.66
        else:
            range_sell_count = 0.99
    range_sell_count *= 5

    good_comments_num = 0
    bad_comments_num = 0
    for comment in item['commentList']:
        if comment['star'] > 3:
            good_comments_num += 1.5 if comment['isPlus'] else 1
        else:
            bad_comments_num += 1.5 if comment['isPlus'] else 1
    # 设定最小值为3
    if good_comments_num < bad_comments_num:
        upper = 3
    else:
        upper = good_comments_num - bad_comments_num
    comments_num = upper / 6

    recom = round((range_sell_count * 0.4 + comments_num * 0.6), 1)
    if recom < 2:
        recom += 1
    print(recom)
    item['recom'] = recom


def __get_item_data(item):
    data = dict()
    for comment in item['commentList']:
        product_type = comment['productType']
        if product_type not in data:
            data[product_type] = array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        season = util.get_month_from_date(comment['time'])
        data[product_type][season] += 1
    return data


if __name__ == '__main__':
    # print(get_item_season_data('100014348492'))
    item = __get_item_from_redis('63211541338')
    __get_item_recom(item)
