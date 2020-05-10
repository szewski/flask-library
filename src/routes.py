from flask import Flask, render_template, url_for, redirect, request, session, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import User, Book, UserToBook
from werkzeug.security import check_password_hash


app = Flask(__name__)


def get_session(echo=False):
    engine = create_engine('sqlite:///db/database.db', echo=echo)
    DBsession = sessionmaker(bind=engine)
    return DBsession()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/catalog/books')
def books():
    DBsession = get_session()
    books = DBsession.query(Book).all()

    return render_template('catalog.html', books=books)


@app.route('/catalog/books/<int:book_id>')
def book(book_id):
    DBsession = get_session()
    mybook = DBsession.query(Book).filter(Book.id == book_id).one()

    return render_template('book.html', book=mybook)


@app.route('/catalog/books/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'GET':
        return render_template('add_book.html')

    if request.method == 'POST':
        DBsession = get_session()

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

        DBsession.add(new_book)
        DBsession.commit()
        return redirect(url_for('books'))


@app.route('/catalog/books/remove_book', methods=['GET', 'POST'])
def remove_book():
    if request.method == 'GET':
        return render_template('remove_book.html')

    if request.method == 'POST':
        book_id = request.form['id']

        DBsession = get_session()
        DBsession.query(Book). \
            filter(Book.id == book_id) \
            .delete()

        DBsession.commit()

        return redirect(url_for('books'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']

        user_data = session.query(User).filter(User.username == username).one()

        if user_data:
            hashed_password = user_data.password

            if check_password_hash(hashed_password, pwd):
                session['user_id'] = user_data.id
                session['username'] = user_data.username
                return redirect(url_for('index'))

        # Add flash message - Failed to login
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    if request.method == 'POST':
        DBsession = get_session()

        username = request.form['username']
        pwd = request.form['password']
        pwd_repeat = request.form['repeat_password']
        email = request.form['email']
        permission_lvl = 2

        if DBsession.query(User).filter(User.username == username).scalar():
            print('User already exists')
            return render_template('register.html')

        if DBsession.query(User).filter(User.email == email).scalar():
            print('Email already exists')
            return render_template('register.html')

        if pwd != pwd_repeat:
            print('Password doesn\'t match')
            return render_template('register.html')

        new_user = User()

        new_user.username = username
        new_user.password = pwd
        new_user.email = email
        new_user.permission_lvl = permission_lvl

        DBsession.add(new_user)
        DBsession.commit()

        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
