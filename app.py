from flask import Flask
from flask import request
from service import query_category
from service import query_item
from service import search_item
from result import Result
import json

app = Flask(__name__)
default_size = 20


@app.route('/categories')
def categories():
    model = list(query_category.query_first_categories())
    dic = Result(success=True, model=model).get_json()
    return json.dumps(dic, ensure_ascii=False)


@app.route('/category/price')
def category_price_data():
    first_cate = request.args.get('category')
    price_data = query_category.query_category_price_data(first_cate)
    data_values = list()
    for data in price_data:
        data_values.append(data[1])

    res = {
        'cates': [x[0] for x in price_data],
        'max_values': [x[0] for x in data_values],
        'min_values': [x[1] for x in data_values],
        'mid_values': [x[4] for x in data_values]
    }
    return json.dumps(res, ensure_ascii=False)


@app.route('/category/brand')
def category_brand_data():
    first_cate = request.args.get('category')
    brand_data = query_category.query_category_brand_data(first_cate)
    shops_data = list()
    shops = list()
    for item in brand_data:
        shops_data.append({
            'name': item[0],
            'value': item[1]
        })
        shops.append(item[0])
    core_items = shops_data[:3]
    core_items[0]['selected'] = True
    res = {
        'shops': shops,
        'shops_data': shops_data,
        'core_items': core_items
    }
    return json.dumps(res, ensure_ascii=False)


@app.route('/category/time')
def category_time_data():
    first_cate = request.args.get('category')
    top_ten_cate = query_category.query_category_price_data(first_cate)
    time_data = query_category.query_category_time_data(first_cate, top_ten_cate)
    time_data.insert(0, ['product', 'spring', 'summer', 'autumn', 'winter'])
    res = {
        'data': time_data
    }
    return json.dumps(res, ensure_ascii=False)


@app.route('/item/info')
def item_info():
    sku_id = request.args.get('skuId')
    res = query_item.get_item_info(sku_id)
    return json.dumps(res, ensure_ascii=False)


@app.route('/item/data')
def item_data():
    sku_id = request.args.get('skuId')
    res = query_item.get_item_season_data(sku_id)
    return json.dumps(res, ensure_ascii=False)


@app.route('/item/goods')
def item_goods():
    sku_id = request.args.get('skuId')
    res = query_item.get_good_words(sku_id)
    return json.dumps(res, ensure_ascii=False)


@app.route('/item/bads')
def item_bads():
    sku_id = request.args.get('skuId')
    res = query_item.get_bad_words(sku_id)
    return json.dumps(res, ensure_ascii=False)


@app.route('/item/search')
def item_search():
    keyword = request.args.get('keyword')
    size = request.args.get('size')
    if size is None:
        size = default_size
    res = search_item.search_items(keyword, size)
    return json.dumps(res, ensure_ascii=False)


if __name__ == "__main__":
    app.run()
