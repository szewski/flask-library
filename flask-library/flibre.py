from flask import Flask, render_template, url_for, redirect


app = Flask(__name__)


@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    return render_template('index.html')


@app.route('/library', methods=['GET'])
def library():
    return render_template('library.html')


if __name__ == '__main__':
    # pass
    app.run(debug=True)