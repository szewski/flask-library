from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm, AddItemForm
from flask_sqlalchemy import SQLAlchemy
import json


app = Flask(__name__)
app.config['SECRET_KEY'] = '\x17%\x9b\t\xc8Dv\x9e~\xa1o\x0e9"jT\xcf\x1aG\xb3A*r'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(12), nullable=True)
    title = db.Column(db.String(40), nullable=False)
    subtitle = db.Column(db.String(40), nullable=True)
    author = db.Column(db.String(20), nullable=False)
    published = db.Column(db.Integer, nullable=True)
    publisher = db.Column(db.String(20), nullable=True)
    pages = db.Column(db.Integer, nullable=True)
    description = db.Column(db.String(255), nullable=True)
    website = db.Column(db.String(12), nullable=True)

with open('database.json', 'r') as f:
    books = json.load(f)
    books = books['books']


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Pomyślnie zalogowano!', 'success')
        return redirect(url_for('home'))
    return render_template('login.html', title='Zaloguj', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Konto stworzone dla {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Rejestracja', form=form)


@app.route('/account')
def account():
    return render_template('account.html', title='Konto')


@app.route('/catalog')
def catalog():
    return render_template('catalog.html', title='Katalog', books=books)


@app.route('/catalog/item/<int:item_id>')
def item(item_id):
    for book in books:
        if book['isbn'] == str(item_id):
            return render_template('item.html', title='Pozycja', item=book)
    raise ValueError


@app.route('/add_item', methods=['POST', 'GET'])
def add_item():
    form = AddItemForm()
    if form.validate_on_submit():
        return redirect(url_for('catalog'))
    return render_template('add_item.html', title='Dodaj pozycję', form=form)

# @app.errorhandler(Exception)
# def page_not_found(error):
#     return render_template('error.html')


if __name__ == '__main__':
    # pass
    app.run(debug=True)
