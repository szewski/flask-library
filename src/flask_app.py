from functools import wraps

from flask import Flask, render_template, url_for, redirect, request, session, flash, get_flashed_messages, abort, Blueprint
from sqlalchemy import create_engine, or_, and_
from sqlalchemy.orm import sessionmaker
from werkzeug.security import check_password_hash, generate_password_hash

from db_models import User, Book


app = Flask(__name__)
app.config.from_object("config.ProductionConfig")


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)


def get_session(echo=False):
    engine = create_engine('sqlite:///db/database.db', echo=echo)
    db_session = sessionmaker(bind=engine)
    return db_session()


def get_default_context():
    permission_lvl = get_user_auth_lvl()
    context = {'permission_lvl': permission_lvl,
               'user_id': session.get('user_id'),
               'username': session.get('username')}
    return context


def get_user_auth_lvl():
    if not session.get('user_id'):
        return 3

    db_session = get_session()
    user_data = db_session.query(User.permission_lvl) \
                .filter(User.username == session.get('username')) \
                .one()
    return user_data.permission_lvl


def get_borrow_limit(username):
    db_session = get_session()
    user_data = db_session.query(User.book_limit) \
                .filter(User.username == username) \
                .one()
    return user_data.book_limit


def get_borrowed(username):
    db_session = get_session()
    return db_session.query(Book).join(User).filter(User.username == username).all()


def count_borrowed(username):
    return len(get_borrowed(username))


def user_exists(username):
    db_session = get_session()
    return db_session.query(User.id).filter_by(username=username).scalar() is not None


def is_able_to_borrow(username):
    borrow_limit = get_borrow_limit(username)
    if borrow_limit == 0:
        return True
    if count_borrowed(username) < borrow_limit:
        return True
    return False


def is_borrowed(book_id):
    db_session = get_session()
    result = db_session.query(Book) \
        .filter(and_(Book.id == book_id, Book.user_id == None)) \
        .scalar()

    return True if result is None else False


def login_required(lvl=3):
    def frame(func):
        @wraps(func)
        def wrapped_func(*args, **kwargs):
            if get_user_auth_lvl() <= lvl:
                return func(*args, **kwargs)
            else:
                flash('Access denied')
                return redirect('/login')
        return wrapped_func

    return frame


@app.route('/')
@app.route('/index')
def index():
    context = get_default_context()
    return render_template('index.html', **context)


@app.route('/catalog/books')
def books():
    db_session = get_session()
    all_books = db_session.query(Book).all()

    context = get_default_context()
    context['books'] = all_books

    return render_template('catalog.html', **context)


@app.route('/catalog/books/<int:book_id>')
def book(book_id):
    db_session = get_session()
    mybook = db_session.query(Book).filter(Book.id == book_id).scalar()

    if not mybook:
        abort(404)

    context = get_default_context()
    context['book'] = mybook
    return render_template('book.html', **context)


@app.route('/catalog/books/add_book', methods=['GET', 'POST'])
@login_required(lvl=1)
def add_book():
    if request.method == 'GET':
        context = get_default_context()
        return render_template('add_book.html', **context)

    if request.method == 'POST':
        db_session = get_session()

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

        db_session.add(new_book)
        db_session.commit()

        return redirect(url_for('books'))


@app.route('/catalog/books/<int:book_id>/edit', methods=['GET', 'POST'])
@login_required(lvl=1)
def edit_book(book_id):
    if request.method == 'GET':
        db_session = get_session()
        mybook = db_session.query(Book).filter(Book.id == book_id).scalar()

        if not mybook:
            abort(404)

        context = get_default_context()
        context['book'] = mybook
        return render_template('edit_book.html', **context)

    if request.method == 'POST':
        db_session = get_session()

        book = db_session.query(Book).filter(Book.id == book_id).one()
        book.isbn = request.form['isbn']
        book.author = request.form['author']
        book.description = request.form['description']
        book.isbn = request.form['isbn']
        book.pages = request.form['pages']
        book.published = request.form['published']
        book.publisher = request.form['publisher']
        book.subtitle = request.form['subtitle']
        book.title = request.form['title']
        book.website = request.form['website']

        db_session.commit()

        return redirect(f'/catalog/books/{book_id}')


@app.route('/catalog/books/remove_book', methods=['GET', 'POST'])
@login_required(lvl=1)
def remove_book():
    if request.method == 'GET':
        context = get_default_context()
        return render_template('remove_book.html', **context)

    if request.method == 'POST':
        book_id = request.form['book_id']

        db_session = get_session()
        db_session.query(Book). \
            filter(Book.id == book_id) \
            .delete()

        db_session.commit()

        return redirect(url_for('books'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        context = get_default_context()
        context['messages'] = get_flashed_messages()

        return render_template('login.html', **context)

    if request.method == 'POST':
        db_session = get_session()

        username = request.form['username']
        pwd = request.form['password']

        user_data = db_session.query(User).filter(User.username == username).scalar()

        if user_data:
            hashed_password = user_data.password

            if check_password_hash(hashed_password, pwd):
                session['user_id'] = user_data.id
                session['username'] = user_data.username
                return redirect(url_for('index'))

        flash('Wrong email or password.')
        return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        context = get_default_context()
        context['messages'] = get_flashed_messages()

        return render_template('register.html', **context)

    if request.method == 'POST':
        db_session = get_session()

        username = request.form['username']
        pwd = request.form['password']
        pwd_repeat = request.form['repeat_password']
        email = request.form['email']
        permission_lvl = 2
        book_limit = 5

        if db_session.query(User).filter(User.username == username).scalar():
            flash('User already exists')
            return redirect(url_for('register'))

        if db_session.query(User).filter(User.email == email).scalar():
            flash('Email already exists')
            return redirect(url_for('register'))

        if pwd != pwd_repeat:
            flash('Password doesn\'t match')
            return redirect(url_for('register'))

        new_user = User()
        new_user.username = username
        new_user.password = generate_password_hash(pwd)
        new_user.email = email
        new_user.permission_lvl = permission_lvl
        new_user.book_limit = book_limit

        db_session.add(new_user)
        db_session.commit()

        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/page_not_found')
def page_not_found():
    return render_template('404.html')


@app.route('/catalog/books/borrow', methods=["POST"])
@login_required(lvl=2)
def borrow_book():
    db_session = get_session()
    book_id = request.form['borrow_book_id']

    if is_borrowed(book_id):
        return redirect(url_for('book', book_id=book_id))

    if not is_able_to_borrow(session.get('username')):
        return redirect(url_for('book', book_id=book_id))

    db_session.query(Book) \
        .filter(Book.id == book_id) \
        .update({'user_id': session.get('user_id')})
    db_session.commit()

    return redirect(redirect_url())


@app.route('/catalog/books/return', methods=["POST"])
@login_required(lvl=2)
def return_book():
    db_session = get_session()
    book_id = request.form['return_book_id']

    db_session.query(Book) \
        .filter(Book.id == book_id) \
        .update({'user_id': None})
    db_session.commit()

    return redirect(redirect_url())


@app.route('/users')
@login_required(lvl=1)
def users():
    db_session = get_session()
    users = []

    all_users = db_session.query(User).all()
    for user in all_users:
        count_books = db_session.query(Book).filter(Book.user_id == user.id).count()
        users.append({'user': user, 'count_books': count_books})

    context = get_default_context()
    context['users'] = users

    return render_template('users.html', **context)


@app.route('/users/user/<username>')
@login_required(lvl=2)
def user_profile(username):
    context = get_default_context()

    if context['permission_lvl'] == 1:
        pass
    elif username != context['username']:
        abort(401)

    if not user_exists(username):
        abort(404)

    context['profile_username'] = username
    context['borrowed_books'] = get_borrowed(username)
    context['current_user'] = username == session.get('username')
    return render_template('user_profile.html', **context)


@app.route('/users/user/<username>/edit', methods=["GET", "POST"])
@login_required(lvl=2)
def user_profile_edit(username):
    if request.method == 'GET':
        context = get_default_context()
        context['messages'] = get_flashed_messages()

        if context['permission_lvl'] == 1:
            pass
        elif username != context['username']:
            abort(401)

        if not user_exists(username):
            abort(404)

        db_session = get_session()
        user = db_session.query(User).filter(User.username == username).one()

        context['user'] = user

        return render_template('user_profile_edit.html', **context)

    if request.method == 'POST':
        db_session = get_session()

        email = request.form['email']
        book_limit = request.form.get('book_limit')
        permission_lvl = request.form.get('permission_lvl')

        user = db_session.query(User).filter(User.username == username).one()

        user.email = email
        if permission_lvl:
            user.permission_lvl = permission_lvl
        if book_limit:
            user.book_limit = book_limit

        db_session.commit()

        flash('Changes saved')

        return redirect(f'/users/user/{username}/edit')


@app.route('/search_results')
def search_results():
    arg = request.args.get('query')
    db_session = get_session()
    context = get_default_context()

    books = db_session.query(Book).filter(
        or_(
            Book.title.contains(arg),
            Book.author.contains(arg)
        )
    ).all()

    context['books'] = books

    return render_template('search_results.html', **context)


@app.route('/test')
def t_page():
    result = session.get('username')
    return str(result)


if __name__ == '__main__':
    app.run()
