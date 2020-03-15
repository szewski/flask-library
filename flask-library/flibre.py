from flask import Flask, render_template, url_for, redirect, request
from database import Database


app = Flask(__name__)
db = Database('database.json')


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/catalog')
def catalog():
    data = db.read()
    books = data['books']

    context = {'books': books}
    return render_template('catalog.html', **context)


@app.route('/catalog/add_item')
def add_item():
    return render_template('add_item.html')


@app.route('/catalog/add_item_post', methods=['POST'])
def add_item_post():
    new_book = request.form.to_dict()
    data = db.read()

    data['books'].append(new_book)
    db.write(data)

    return f"Book {new_book['title']} added!"


if __name__ == '__main__':
    app.run(debug=True)