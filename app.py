from flask import Flask
import query_category

app = Flask(__name__)


@app.route('/categories')
def categories():
    return query_category.query_first_categories()


if __name__ == "__main__":
    app.run()
