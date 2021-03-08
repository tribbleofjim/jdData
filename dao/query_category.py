import mongo_conn
import setting

conn = mongo_conn.MongoConn(host=setting.mongo_params['host'],
                            user=setting.mongo_params['user'],
                            password=setting.mongo_params['password'],
                            database=setting.mongo_params['database'],
                            collection=setting.mongo_params['collection'])
# _first_categories = set()
_first_categories = {'美妆护肤', '玩具乐器', '运动户外', '手机通讯', '文娱', '母婴', '教育培训', '鞋靴', '宠物生活', '食品饮料', '家具日用',
                     '电脑、办公', '数码', '图书', '汽车用品', '服饰内衣', '医疗保健', '家庭清洁/纸品', '二手商品', '厨具', '农资园艺', '家具',
                     '汽车', '箱包皮具', '礼品', '钟表', '酒类', '个人护理', '家用电器', '生鲜', '本地生活/旅游出行', '家纺', '家装建材'}


def query_first_categories():
    if len(_first_categories) != 0:
        return _first_categories

    categories = conn.find(projection={'productClass': 1, '_id': 0})
    for category in categories:
        product_class = category['productClass']
        if product_class is None:
            continue
        first_class = product_class.split('-')[0]
        _first_categories.add(first_class)
    return _first_categories


if __name__ == '__main__':
    res = query_first_categories()
    for cate in res:
        print(cate)
