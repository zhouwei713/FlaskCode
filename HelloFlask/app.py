# coding = utf-8
"""
@author: zhou
@time:2019/11/5 11:13
@File: app.py
"""

from flask import Flask, url_for

app = Flask(__name__)


@app.route('/hello')
@app.route('/say', endpoint='new')
def hello():
    return 'Hello Flask!'


@app.route('/user/', defaults={'name': '陌生人'})
@app.route('/user/<name>')
def welcome(name):
    print(url_for('hello'))
    return '<h1>Hello, %s!</h1>' % name


if __name__ == '__main__':
    app.run(debug=True)
