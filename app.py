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


if __name__ == "__main__":
    app.run()
