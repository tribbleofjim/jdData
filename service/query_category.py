import mongo_conn
import setting
import util
from array import array
import _thread

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
_first_categories = ['美妆护肤', '农资园艺', '教育培训', '家具日用', '礼品', '图书', '玩具乐器', '手机通讯', '文娱', '母婴', '鞋靴', '宠物生活', '食品饮料',
                     '电脑、办公', '数码', '汽车用品', '服饰内衣', '医疗保健', '家庭清洁/纸品', '二手商品', '厨具', '家具', '运动户外',
                     '汽车', '箱包皮具', '钟表', '酒类', '个人护理', '家用电器', '生鲜', '本地生活/旅游出行', '家纺', '家装建材']


def query_first_categories():
    if len(_first_categories) != 0:
        return _first_categories
    else:
        categories = analyze_conn.find_one(query={'categories': {'$exists': True}})
        if categories is None or len(categories) == 0:
            analyze_conn.add_one({
                'categories': _first_categories
            })
            return categories


def get_categories():
    categories = data_conn.find(projection={'productClass': 1, '_id': 0})
    for category in categories:
        product_class = category['productClass']
        if product_class is None:
            continue
        first_class = product_class.split('-')[0]
        _first_categories.add(first_class)
    return _first_categories


def _query_category_data(first_cate):
    cate_data = analyze_conn.find_one(query={'first_cate': {'$regex': '^' + first_cate}, 'all_sum': {'$exists': True}})
    if cate_data is None:
        _thread.start_new_thread(__get_category_statistic, (first_cate, 100))
        return "很抱歉，当前分类的数据暂时未计算"
    return cate_data


def query_category_price_data(first_cate):
    res = analyze_conn.find_one(query={'first_cate': {'$regex': '^' + first_cate}, 'price_data': {'$exists': True}})
    if res is None:
        cate_data = _query_category_data(first_cate)
        prices = cate_data['prices']
        res = sorted(prices.items(), key=lambda item: item[1][3], reverse=True)[:10]
        for cate in res:
            for i in range(0, 5):
                cate[1][i] = round(cate[1][i], 2)
        analyze_conn.add_one({
            'first_cate': first_cate,
            'price_data': res
        })
        return res
    return res['price_data']


def query_category_brand_data(first_cate):
    res = analyze_conn.find_one(query={'first_cate': {'$regex': '^' + first_cate}, 'brand_data': {'$exists': True}})
    if res is None:
        cate_data = _query_category_data(first_cate)
        shops = cate_data['shops']
        res = sorted(shops.items(), key=lambda item: item[1], reverse=True)[:10]
        analyze_conn.add_one({
            'first_cate': first_cate,
            'brand_data': res
        })
        return res
    return res['brand_data']


def query_category_time_data(first_cate, top_ten_cate):
    res = analyze_conn.find_one(query={'first_cate': {'$regex': '^' + first_cate}, 'time_data': {'$exists': True}})
    if res is None:
        cate_data = _query_category_data(first_cate)
        season_cates = cate_data['season_cates']
        res = list()
        for cate, items in season_cates.items():
            if cate in top_ten_cate:
                lst = list()
                lst.append(cate)
                for x in items:
                    lst.append(x)
                res.append(lst)
        analyze_conn.add_one({
            'first_cate': first_cate,
            'time_data': res
        })
        return res
    return res['time_data']


def __get_category_statistic(first_cate, batch_size):
    prices = dict()  # [max, min, sum, size, mid]
    shops = dict()  # {'shop_name': num}
    season_cates = dict()  # {'cate': [spring, summer, autumn, winter]}
    sell_count = [1, 2147483647]  # [max_sell_count, min_sell_count]
    skip_num = 0
    product_list = ['']
    i = 0
    while len(product_list) > 0:
        product_list = list(data_conn.find(query={'productClass': {'$regex': '^' + first_cate}})
                            .skip(skip_num).limit(batch_size))
        __category_statistic(product_list, prices, shops, season_cates, sell_count)
        i += 1
        skip_num += batch_size
        print('====== cate: ' + first_cate + ', batch:' + str(i) + ', num:' + str(skip_num) + ' =====')

    util.array_to_list(prices)
    util.array_to_list(season_cates)

    analyze_data = {
        'first_cate': first_cate,
        'prices': prices,
        'shops': shops,
        'season_cates': season_cates,
        'sell_count': sell_count,
        'all_sum': True
    }
    analyze_conn.add_one(data=analyze_data)


def __category_statistic(products, prices, shops, season_cates, sell_count):
    for product in products:
        cates = product['productClass'].split('-')
        if len(cates) < 3:
            continue
        second_cate = cates[2]

        product_sell_count = util.get_sell_count(product['sellCount'])
        if product_sell_count > 0:
            sell_count[0] = max(sell_count[0], product_sell_count)
            sell_count[1] = min(sell_count[1], product_sell_count)

        try:
            price = float(product['price'][:-1])
        except(TypeError, ValueError):
            continue
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
            season_cates[second_cate] = array('i', [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        __get_season_cates(season_cates, second_cate, product)

        shop = product['shop']
        if shop is None:
            continue
        if shop.find('.') != -1:
            shop = shop.replace('.', '')
        if shop not in shops:
            shops[shop] = 0
        shops[shop] += 1


def __get_season_cates(season_cates, cate, product):
    comments = product['commentList']
    for comment in comments:
        time = comment['time']
        season = util.get_month_from_date(time)
        season_cates[cate][season] += 1


if __name__ == '__main__':
    # 预处理所有的数据
    query_first_categories()
    for _first_cate in _first_categories:
        __get_category_statistic(_first_cate, 100)
        query_category_brand_data(_first_cate)
        top_ten_cate = [x[0] for x in query_category_price_data(_first_cate)]
        query_category_time_data(_first_cate, top_ten_cate)
