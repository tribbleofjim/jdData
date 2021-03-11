from flask import Flask
from service import query_category
from result import Result
import json

app = Flask(__name__)


@app.route('/categories')
def categories():
    model = list(query_category.query_first_categories())
    dic = Result(success=True, model=model).get_json()
    return json.dumps(dic, ensure_ascii=False)


@app.route('/category/price/<first_cate>')
def category_price_data(first_cate):
    price_data = query_category.query_category_price_data(first_cate)
    data_values = list()
    for data in price_data:
        data_values.append(data[1])
    # data_values = price_data.values()

    res = {
        'cates': [x[0] for x in price_data],
        'max_values': [x[0] for x in data_values],
        'min_values': [x[1] for x in data_values],
        'mid_values': [x[4] for x in data_values]
    }
    return json.dumps(res, ensure_ascii=False)


@app.route('/category/brand/<first_cate>')
def category_brand_data(first_cate):
    brand_data = query_category.query_category_brand_data(first_cate)
    shops_data = list()
    for shop, num in shops_data.items():
        shops_data.append({
            'name': shop,
            'value': num
        })
    res = {
        'shops': brand_data.keys(),
        'shops_data': shops_data,
        'core_items': shops_data[:5]
    }
    return json.dumps(res, ensure_ascii=False)


@app.route('/category/time/<first_cate>')
def category_time_data(first_cate):
    time_data = query_category.query_category_time_data(first_cate)
    time_data.insert(0, ['product', 'spring', 'summer', 'autumn', 'winter'])
    res = {
        'data': time_data
    }
    return json.dumps(res, ensure_ascii=False)


if __name__ == "__main__":
    app.run()
