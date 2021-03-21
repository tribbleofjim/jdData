from elasticsearch import Elasticsearch
import setting

es = Elasticsearch()


def search_items(keyword, size=20, price_interval=None):
    if price_interval is None:
        res = es.search(index=setting.es_index, body={'query': {'match': {'title': keyword}},
                                                      '_source': ['title', 'price', 'productClass', 'skuId'],
                                                      'size': size})
    else:
        interval = price_interval.split('-')
        if len(interval) < 2:
            res = es.search(index=setting.es_index, body={'query': {'match': {'title': keyword}},
                                                          '_source': ['title', 'price', 'productClass', 'skuId'],
                                                          'size': size})
        else:
            res = es.search(index=setting.es_index, body={'query': {'bool': {'must': [{'match': {'title': keyword}}, {
                'range': {'price': {'gte': int(interval[0]), 'lte': int(interval[1])}}}]}},
                                                          '_source': ['title', 'price', 'productClass', 'skuId'],
                                                          'size': size})
    return [x['_source'] for x in res['hits']['hits']]


if __name__ == '__main__':
    test_res = search_items('洗衣机', 20, '100-2000')
    for test_r in test_res:
        print(test_r)
