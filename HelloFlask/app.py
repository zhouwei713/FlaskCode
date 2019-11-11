# coding = utf-8
"""
@author: zhou
@time:2019/11/5 11:13
@File: app.py
"""

from flask import Flask, url_for, request

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


@app.route('/test/')
def test_view():
    query = 'Flask'
    if request.args:
        query = request.args.get('name', 'Flask')
    host = request.host
    path = request.full_path
    cookie = request.cookies
    method = request.method
    return """
    <h1>
    <p>query string: %s</p>
    <p>host: %s</p>
    <p>path: %s</p>
    <p>cookies: %s</p>
    <p>method: %s</p>
    </h1>
    """ % (query, host, path, cookie, method)


if __name__ == '__main__':
    app.run(debug=True)
