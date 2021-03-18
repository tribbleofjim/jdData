from elasticsearch import Elasticsearch

es = Elasticsearch()

index = 'jingdong'


def search_items(keyword, size):
    res = es.search(index=index, body={'query': {'match': {'title': keyword}},
                                       '_source': ['title', 'price', 'productClass', 'skuId'],
                                       'size': size})
    return [x['_source'] for x in res['hits']['hits']]


if __name__ == '__main__':
    test_res = search_items('洗衣机', 20)
    for test_r in test_res:
        print(test_r)
