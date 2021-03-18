import jieba.analyse
import mongo_conn
import redis
import ast
import setting


data_conn = mongo_conn.MongoConn(host=setting.mongo_params['host'],
                                 user=setting.mongo_params['user'],
                                 password=setting.mongo_params['password'],
                                 database=setting.mongo_params['database'],
                                 collection=setting.mongo_params['data_collection'])

r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

jieba.analyse.set_stop_words("./service/text_words/baidu_stopwords.txt")


def jieba_test():
    jieba.analyse.set_stop_words("./text_words/baidu_stopwords.txt")
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
    item = _get_item_from_redis(sku_id)
    del item['commentList']
    return item


def get_good_words(sku_id):
    item = _get_item_from_redis(sku_id)
    comments = item['commentList']
    sentence = ''
    for comment in comments:
        if comment['star'] >= 3:
            sentence += comment['content']
    words = jieba.analyse.textrank(sentence, topK=10, withWeight=True)
    return [[x[0], round(x[1], 3) * 1000] for x in words]


def get_bad_words(sku_id):
    item = _get_item_from_redis(sku_id)
    comments = item['commentList']
    sentence = ''
    for comment in comments:
        if comment['star'] < 3:
            sentence += comment['content']
    words = jieba.analyse.textrank(sentence, topK=10, withWeight=True)
    return [[x[0], round(x[1], 3) * 1000] for x in words]


def _get_item_from_redis(sku_id):
    item = r.get(sku_id)
    if item is None:
        item = data_conn.find_one(query={'skuId': sku_id}, projection={'_id': 0})
        r.set(sku_id, item)
    else:
        item = ast.literal_eval(item)
    r.expire(sku_id, 1800)
    return item


if __name__ == '__main__':
    my_res = get_item_info('100014348492')
    print(my_res)
