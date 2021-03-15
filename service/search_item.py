from elasticsearch import Elasticsearch

es = Elasticsearch()

index = 'jingdong'

if __name__ == '__main__':
    res = es.search(index=index, body={'query': {'match': {'title': '充电宝'}},
                                       '_source': ['title', 'price', 'productClass', 'skuId'],
                                       'size': 20})
    for hit in res['hits']['hits']:
        print(hit)
