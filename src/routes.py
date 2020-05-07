from flask import Flask, render_template, url_for, redirect, request, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import User, Book, UserToBook


app = Flask(__name__)


def get_session(echo=False):
    engine = create_engine('sqlite:///db/database.db', echo=echo)
    session = sessionmaker(bind=engine)
    return session()


@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/catalog/books')
def books():
    session = get_session()
    books = session.query(Book).all()

    return render_template('catalog.html', books=books)


@app.route('/catalog/books/<int:book_id>')
def book(book_id):
    session = get_session()
    mybook = session.query(Book).filter(Book.id == book_id).one()

    return render_template('book.html', book=mybook)


@app.route('/catalog/books/add_book')
def add_book_form():
    return render_template('add_book_form.html')


@app.route('/catalog/books/add_book_post', methods=['POST'])
def add_book_post():
    session = get_session()

    new_book = Book()
    new_book.isbn = request.form['isbn']
    new_book.author = request.form['author']
    new_book.description = request.form['description']
    new_book.isbn = request.form['isbn']
    new_book.pages = request.form['pages']
    new_book.published = request.form['published']
    new_book.publisher = request.form['publisher']
    new_book.subtitle = request.form['subtitle']
    new_book.title = request.form['title']
    new_book.website = request.form['website']

    session.add(new_book)
    session.commit()
    return redirect(url_for('books'))


@app.route('/catalog/books/remove_book')
def remove_book_form():
    return render_template('remove_book_form.html')


@app.route('/catalog/books/remove_book_post', methods=['POST'])
def remove_book_post():
    book_id = request.form['id']

    session = get_session()
    session.query(Book). \
        filter(Book.id == book_id) \
        .delete()

    session.commit()

    return redirect(url_for('books'))


if __name__ == '__main__':
    app.run(debug=True)
