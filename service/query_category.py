import mongo_conn
import setting
import numpy as np

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
# _first_categories = set()
_first_categories = {'美妆护肤', '玩具乐器', '运动户外', '手机通讯', '文娱', '母婴', '教育培训', '鞋靴', '宠物生活', '食品饮料', '家具日用',
                     '电脑、办公', '数码', '图书', '汽车用品', '服饰内衣', '医疗保健', '家庭清洁/纸品', '二手商品', '厨具', '农资园艺', '家具',
                     '汽车', '箱包皮具', '礼品', '钟表', '酒类', '个人护理', '家用电器', '生鲜', '本地生活/旅游出行', '家纺', '家装建材'}


def query_first_categories():
    if len(_first_categories) != 0:
        return _first_categories

    categories = data_conn.find(projection={'productClass': 1, '_id': 0})
    for category in categories:
        product_class = category['productClass']
        if product_class is None:
            continue
        first_class = product_class.split('-')[0]
        _first_categories.add(first_class)
    return _first_categories


def query_second_cate_products(first_cate):
    products = data_conn.find(query={'productClass': {'$regex': '^' + first_cate}}).limit(100)
    return products


def category_statistic(first_cate):
    products = data_conn.find(query={'productClass': {'$regex': '^' + first_cate}}).limit(100)
    mid_price, min_price, max_price, size, sum_price = 0
    shops = dict()
    season_cates = dict()
    for product in products:
        size += 1
        price = product['price']
        sum_price += price
        max_price = price if price > max_price else max_price
        min_price = price if price < min_price else min_price

        shop = product['shop']
        if shop not in shops:
            shops[shop] = 0
        shops[shop] += 1

        cates = product['productClass'].split('-')
        if len(cates) < 3:
            continue
        second_cate = cates[2]
        if second_cate not in season_cates.keys():
            season_cates[second_cate] = np.array([1, 4])
        get_season_cates(season_cates, second_cate, product)
    mid_price = sum_price / size


def get_season_cates(season_cates, cate, product):
    comments = product['comments']
    for comment in comments:
        date = comment['date']
        season = get_season_from_date(date)
        season_cates[cate][season] += 1


def get_season_from_date(date):
    return ''


if __name__ == '__main__':
    res = query_second_cate_products('手机通讯')
    for prod in res:
        print(prod)
