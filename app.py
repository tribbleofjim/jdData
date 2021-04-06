from flask import request, session
from service import query_category
from service import query_item
from service import search_item
from result import Result
from mysql_conn import *
import util
import json


@app.route('/login', methods=['POST'])
def login():
    data = request.json['params']
    print(data)
    phone = data['phone']
    password = data['password']
    table_user = MapleUser.query.filter(MapleUser.phone == phone).first()
    if table_user is None or table_user.password != password:
        return json.dumps(Result(success=False, message='用户名或密码错误', model=None).get_json(), ensure_ascii=False)
    # 设置session
    session['phone'] = phone
    return json.dumps(Result(success=True, message='登录成功', model=None).get_json(), ensure_ascii=False)


@app.route('/exitLogin', methods=['POST'])
def exit_login():
    data = request.json['params']
    phone = data['phone']
    session['phone'] = None
    return json.dumps(Result(success=True, message='退出登录成功', model=None).get_json(), ensure_ascii=False)


@app.route('/register', methods=['POST'])
def register():
    data = request.json['params']
    phone = data['phone']
    password = data['password']
    nickname = data['nickname']
    auth = 1
    user = MapleUser(phone, nickname, password, auth)
    db.session.add(user)
    db.session.commit()
    return json.dumps(Result(success=True, message='注册成功', model=None).get_json(), ensure_ascii=False)


@app.route('/modifyPassword', methods=['POST'])
def modify_password():
    data = request.json['params']
    phone = data['phone']
    old_password = data['oldPass']
    new_password = data['newPass']
    user = MapleUser.query.filter(MapleUser.phone == phone).first()
    if user is None:
        return json.dumps(Result(success=False, message='不存在该用户', model=None).get_json(), ensure_ascii=False)
    if old_password != user.password:
        return json.dumps(Result(success=False, message='密码错误', model=None).get_json(), ensure_ascii=False)
    user.password = new_password
    db.session.commit()
    return json.dumps(Result(success=True, message='修改密码成功', model=None).get_json(), ensure_ascii=False)


@app.route('/modifyNickname', methods=['POST'])
def modify_nickname():
    data = request.json['params']
    phone = data['phone']
    password = data['password']
    new_nickname = data['newNickname']
    user = MapleUser.query.filter(MapleUser.phone == phone).first()
    if user is None:
        return json.dumps(Result(success=False, message='不存在该用户', model=None).get_json(), ensure_ascii=False)
    if password != user.password:
        return json.dumps(Result(success=False, message='密码错误', model=None).get_json(), ensure_ascii=False)
    user.nickname = new_nickname
    db.session.commit()
    return json.dumps(Result(success=True, message='修改昵称成功', model=None).get_json(), ensure_ascii=False)


@app.route('/categories')
def categories():
    model = query_category.query_first_categories()
    dic = Result(success=True, model=model).get_json()
    return json.dumps(dic, ensure_ascii=False)


@app.route('/category/price')
def category_price_data():
    first_cate = util.get_first_cate(request.args.get('category'))
    price_data = query_category.query_category_price_data(first_cate)
    data_values = list()
    for data in price_data:
        data_values.append(data[1])

    res = {
        'cates': [x[0] for x in price_data],
        'max_values': [int(x[0]) for x in data_values],
        'min_values': [int(x[1]) for x in data_values],
        'mid_values': [int(x[4]) for x in data_values]
    }
    return json.dumps(res, ensure_ascii=False)


@app.route('/category/brand')
def category_brand_data():
    first_cate = util.get_first_cate(request.args.get('category'))
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
    if len(core_items) >= 1:
        core_items[0]['selected'] = True
    res = {
        'shops': shops,
        'shops_data': shops_data,
        'core_items': core_items
    }
    return json.dumps(res, ensure_ascii=False)


@app.route('/category/time')
def category_time_data():
    first_cate = util.get_first_cate(request.args.get('category'))
    top_ten_cate = [x[0] for x in query_category.query_category_price_data(first_cate)]
    time_data = query_category.query_category_time_data(first_cate, top_ten_cate)
    time_data.insert(0, ['product', '1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月'])
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
    price_interval = request.args.get('price_interval')
    if size is None:
        size = 20
    res = search_item.search_items(keyword, size, price_interval)
    return json.dumps(res, ensure_ascii=False)


if __name__ == "__main__":
    app.run()
