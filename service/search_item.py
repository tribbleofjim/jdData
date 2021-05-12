from elasticsearch import Elasticsearch
import setting
import time

es = Elasticsearch()


def search_items(keyword, size=20, price_interval=None):
    interval = __get_interval(price_interval)
    s = len(interval)
    if s == 0:
        res = es.search(index=setting.es_index, body={'query': {'match': {'title': keyword}},
                                                      '_source': ['title', 'price', 'productClass', 'skuId'],
                                                      'size': size})
    elif s == 1:
        res = es.search(index=setting.es_index, body={'query': {'bool': {'must': [{'match': {'title': keyword}}, {
            'range': {'price': {'gte': int(interval[0])}}}]}},
                                                      '_source': ['title', 'price', 'productClass', 'skuId'],
                                                      'size': size})
    else:
        res = es.search(index=setting.es_index, body={'query': {'bool': {'must': [{'match': {'title': keyword}}, {
            'range': {'price': {'gte': int(interval[0]), 'lte': int(interval[1])}}}]}},
                                                      '_source': ['title', 'price', 'productClass', 'skuId'],
                                                      'size': size})
    return [x['_source'] for x in res['hits']['hits']]


def search_items_test(keyword, size=20, price_interval=None):
    interval = __get_interval(price_interval)
    s = len(interval)
    if s == 0:
        res = es.search(index=setting.es_index, body={'query': {'match': {'title': keyword}},
                                                      '_source': ['title', 'price', 'productClass', 'skuId', 'sellCount', 'commentList'],
                                                      'size': size})
    elif s == 1:
        res = es.search(index=setting.es_index, body={'query': {'bool': {'must': [{'match': {'title': keyword}}, {
            'range': {'price': {'gte': int(interval[0])}}}]}},
                                                      '_source': ['title', 'price', 'productClass', 'skuId', 'sellCount', 'commentList'],
                                                      'size': size})
    else:
        res = es.search(index=setting.es_index, body={'query': {'bool': {'must': [{'match': {'title': keyword}}, {
            'range': {'price': {'gte': int(interval[0]), 'lte': int(interval[1])}}}]}},
                                                      '_source': ['title', 'price', 'productClass', 'skuId', 'sellCount', 'commentList'],
                                                      'size': size})
    return [x['_source'] for x in res['hits']['hits']]


def __get_interval(price_interval):
    interval = []
    try:
        if price_interval is None:
            return []
        if price_interval.endswith('以上'):
            interval.append(int(price_interval[:-2]))
        else:
            interval = price_interval.split('-')
            if len(interval) < 2:
                return []
            interval[0] = int(interval[0])
            interval[1] = int(interval[1])
    except TypeError:
        return []
    return interval


if __name__ == '__main__':
    time_start = time.time()
    test_res = search_items('口红', 10, '100-2000')
    time_end = time.time()
    for test_r in test_res:
        print(test_r)
    print(time_end - time_start)
