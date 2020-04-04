from flask import Flask, render_template, url_for, redirect, request
from db.db_control import SQLiteDb
from pathlib import Path

app = Flask(__name__)
db = SQLiteDb(Path('db/database.db'))


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/catalog')
def catalog():
    books = db.get_data('SELECT * FROM "books"')
    print(books)
    context = {'books': books}
    return render_template('catalog.html', **context)


@app.route('/catalog/add_book')
def add_book():
    return render_template('add_book.html')


@app.route('/catalog/add_book_post', methods=['POST'])
def add_book_post():
    new_book = request.form.to_dict()
    print(new_book)
    query = """
    INSERT INTO "books" VALUES
        (NULL, :author, :description, :isbn, :pages, 
        :published, :publisher, :subtitle, :title, :website)
    """
    db.write_data(query, new_book)

    return redirect(url_for('catalog'))


if __name__ == '__main__':
    app.run(debug=True)