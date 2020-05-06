from flask import Flask, render_template, url_for, redirect, request, g
import sqlite3
from pathlib import Path

app = Flask(__name__)
DATABASE = Path('db/database.db')


def query_add_book(new_book):
    query = """
    INSERT INTO "books" VALUES
        (NULL, :author, :description, :isbn, :pages, 
        :published, :publisher, :subtitle, :title, :website)
    """
    query_write_db(query, new_book)


def query_get_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def query_write_db(query, args=(), one=False):
    conn = get_db()
    conn.execute(query, args)
    conn.commit()
    conn.close()


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/catalog/books')
def books():
    all_books = query_get_db('SELECT * FROM "books"')
    context = {'books': all_books}
    return render_template('catalog.html', **context)


@app.route('/catalog/books/<int:book_id>')
def book(book_id):
    params = {'book_id': book_id}
    mybook = query_get_db('SELECT * FROM "books" WHERE "id" = :book_id', params, one=True)

    return render_template('book.html', book=mybook)


@app.route('/catalog/books/add_book')
def add_book():
    return render_template('add_book.html')


@app.route('/catalog/books/add_book_post', methods=['POST'])
def add_book_post():
    new_book = request.form.to_dict()
    query_add_book(new_book)
    return redirect(url_for('books'))


@app.route('/catalog/books/remove_book_post', methods=['POST'])
def remove_book_post():
    # new_book = request.form.to_dict()

    return redirect(url_for('books'))


if __name__ == '__main__':
    app.run(debug=True)