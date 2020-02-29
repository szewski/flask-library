from flask import Flask, render_template, url_for
import json

app = Flask(__name__)

with open('database.json', 'r') as f:
    books = json.load(f)
    books = books['books']


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/login')
def login():
    return render_template('login.html', title='Zaloguj')


@app.route('/register')
def register():
    return render_template('register.html', title='Rejestracja')


@app.route('/account')
def account():
    return render_template('account.html', title='Konto')


@app.route('/catalog')
def catalog():
    return render_template('catalog.html', title='Katalog', books=books)


@app.route('/item')
def item():
    return render_template('item.html', title='Pozycja')


if __name__ == '__main__':
    # pass
    app.run(debug=True)
