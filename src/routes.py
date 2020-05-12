from flask import Flask, render_template, url_for, redirect, request, session, g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models import User, Book
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.secret_key = 'super_tajny_klucz_123'


def get_username():
    if session:
        return session['username']
    return None


def default_context():
    permission_lvl = get_user_auth_lvl()
    context = {'permission_lvl': permission_lvl,
               'user_id': get_user_id(),
               'username': get_username()}
    return context


def get_user_id():
    if not session:
        return None

    DBsession = get_session()
    user_data = DBsession.query(User) \
                .filter(User.username == session['username']) \
                .one()
    return user_data.id


def get_user_auth_lvl():
    if not session:
        return 3

    DBsession = get_session()
    user_data = DBsession.query(User) \
                .filter(User.username == session['username']) \
                .one()
    return user_data.permission_lvl


def authorized(lvl=3):
    if get_user_auth_lvl() <= lvl:
        return True
    return False


def get_session(echo=False):
    engine = create_engine('sqlite:///db/database.db', echo=echo)
    DBsession = sessionmaker(bind=engine)
    return DBsession()


@app.route('/')
@app.route('/index')
def index():
    context = default_context()
    return render_template('index.html', **context)


@app.route('/catalog/books')
def books():
    DBsession = get_session()
    books = DBsession.query(Book).all()

    context = default_context()
    context['books'] = books

    return render_template('catalog.html', **context)


@app.route('/catalog/books/<int:book_id>')
def book(book_id):
    DBsession = get_session()
    mybook = DBsession.query(Book).filter(Book.id == book_id).one()

    context = default_context()
    context['book'] = mybook
    return render_template('book.html', **context)


@app.route('/catalog/books/add_book', methods=['GET', 'POST'])
def add_book():
    if not authorized(1):
        return access_denied()

    if request.method == 'GET':
        context = default_context()
        return render_template('add_book.html', **context)

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
    if not authorized(1):
        return access_denied()

    if not session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        context = default_context()
        return render_template('remove_book.html', **context)

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
        context = default_context()
        return render_template('login.html', **context)

    if request.method == 'POST':
        DBsession = get_session()

        username = request.form['username']
        pwd = request.form['password']

        user_data = DBsession.query(User).filter(User.username == username).one()

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
        context = default_context()
        return render_template('register.html', **context)

    if request.method == 'POST':
        DBsession = get_session()
        err = False

        username = request.form['username']
        pwd = request.form['password']
        pwd_repeat = request.form['repeat_password']
        email = request.form['email']
        permission_lvl = 2

        if DBsession.query(User).filter(User.username == username).scalar():
            print('User already exists')
            err = True

        if DBsession.query(User).filter(User.email == email).scalar():
            print('Email already exists')
            err = True

        if pwd != pwd_repeat:
            print('Password doesn\'t match')
            err = True

        if err:
            context = default_context()
            return render_template('register.html', **context)

        new_user = User()
        new_user.username = username
        new_user.password = generate_password_hash(pwd)
        new_user.email = email
        new_user.permission_lvl = permission_lvl

        DBsession.add(new_user)
        DBsession.commit()

        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/access_denied')
def access_denied():
    context = default_context()
    return render_template('access_denied.html', **context)


@app.route('/catalog/books/borrow', methods=["POST"])
def borrow_book():
    if not authorized(2):
        return access_denied()

    if not session:
        return redirect(url_for('login'))

    DBsession = get_session()
    book_id = request.form['borrow_book_id']

    update = DBsession.query(Book) \
                .filter(Book.id == book_id) \
                .update({'user_id': get_user_id()})
    DBsession.commit()

    return redirect(url_for('books'))


@app.route('/catalog/books/return', methods=["POST"])
def return_book():
    if not authorized(2):
        return access_denied()

    if not session:
        return redirect(url_for('login'))

    DBsession = get_session()
    book_id = request.form['return_book_id']

    update = DBsession.query(Book) \
                .filter(Book.id == book_id) \
                .update({'user_id': None})
    DBsession.commit()

    return redirect(url_for('books'))


if __name__ == '__main__':
    app.run(debug=True)
