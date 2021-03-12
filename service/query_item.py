import jieba.analyse
import mongo_conn
import setting


data_conn = mongo_conn.MongoConn(host=setting.mongo_params['host'],
                                 user=setting.mongo_params['user'],
                                 password=setting.mongo_params['password'],
                                 database=setting.mongo_params['database'],
                                 collection=setting.mongo_params['data_collection'])

jieba.analyse.set_stop_words("./text_words/baidu_stopwords.txt")


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
    item = data_conn.find_one({'skuId': sku_id}, projection={'_id': 0})
    del item['commentList']
    return item


def get_good_words(sku_id):
    item = data_conn.find_one({'skuId': sku_id})
    comments = item['commentList']
    sentence = ''
    for comment in comments:
        if comment['star'] >= 3:
            sentence += comment['content']
    words = jieba.analyse.textrank(sentence, topK=10, withWeight=True)
    return [[x[0], round(x[1], 3) * 1000] for x in words]


def get_bad_words(sku_id):
    item = data_conn.find_one({'skuId': sku_id})
    comments = item['commentList']
    sentence = ''
    for comment in comments:
        if comment['star'] < 3:
            sentence += comment['content']
    words = jieba.analyse.textrank(sentence, topK=10, withWeight=True)
    return [[x[0], round(x[1], 3) * 1000] for x in words]


if __name__ == '__main__':
    my_res = get_item_info('100014348492')
    print(my_res)
