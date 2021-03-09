import mongo_conn
import setting
from array import array
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


def get_category_statistic(first_cate, batch_size):
    prices = dict()  # [max, min, sum, size, mid]
    shops = dict()  # {'shop_name': num}
    season_cates = dict()  # {'cate': [spring, summer, autumn, winter]}
    skip_num = 0
    product_list = ['']
    # i = 0
    while len(product_list) > 0:
        # while i < 1:
        product_list = list(data_conn.find(query={'productClass': {'$regex': '^' + first_cate}})
                            .skip(skip_num).limit(batch_size))
        category_statistic(product_list, prices, shops, season_cates)
        skip_num += batch_size
        # i += 1

    array_to_list(prices)
    array_to_list(season_cates)

    analyze_data = {
        'first_cate': first_cate,
        'prices': prices,
        'shops': shops,
        'season_cates': season_cates
    }
    analyze_conn.add_one(data=analyze_data)


def array_to_list(target_dict):
    for key, value in target_dict.items():
        value = list(value)
        target_dict[key] = value


def category_statistic(products, prices, shops, season_cates):
    for product in products:
        cates = product['productClass'].split('-')
        if len(cates) < 3:
            continue
        second_cate = cates[2]

        price = float(product['price'][:-1])
        if price is not None:
            if second_cate not in prices.keys():
                prices[second_cate] = array('f', [0., 1000000., 0., 0., 0.])
            second_cate_data = prices[second_cate]
            if price > second_cate_data[0]:
                second_cate_data[0] = price
            if price < second_cate_data[1]:
                second_cate_data[1] = price
            second_cate_data[2] += price
            second_cate_data[3] += 1
            second_cate_data[4] = second_cate_data[2] / second_cate_data[3]

        if second_cate not in season_cates.keys():
            season_cates[second_cate] = array('i', [0, 0, 0, 0])
        get_season_cates(season_cates, second_cate, product)

        shop = product['shop']
        if shop.find('.') != -1:
            shop = shop.replace('.', '')
        if shop not in shops:
            shops[shop] = 0
        shops[shop] += 1
    print(prices)
    print(shops)
    print(season_cates)


def get_season_cates(season_cates, cate, product):
    comments = product['commentList']
    for comment in comments:
        time = comment['time']
        season = get_season_from_date(time)
        season_cates[cate][season] += 1


def get_season_from_date(date):
    if date is not None:
        try:
            month = date.split('-')[1]
            if month.startswith('0'):
                month = month[1:]
            m = int(month)
            if 1 <= m <= 3:
                return 0
            elif 4 <= m <= 6:
                return 1
            elif 7 <= m <= 9:
                return 2
            else:
                return 3
        except IndexError as e:
            print(e)
            return 0


if __name__ == '__main__':
    get_category_statistic('美妆护肤', 100)
