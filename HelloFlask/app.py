# coding = utf-8
"""
@author: zhou
@time:2019/11/5 11:13
@File: app.py
"""

from flask import Flask, url_for, request, session, redirect
from urllib.parse import urlparse

app = Flask(__name__)
app.secret_key = 'Very Hard Secret'


def check_next(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    return ref_url.netloc == test_url.netloc


@app.route('/login/')
def login():
    session['loginID'] = 'admin'
    target = request.args.get('next')
    if check_next(target):
        return redirect(target)
    return redirect(url_for('hello'))


@app.route('/needlogin1/')
def needLogin1():
    if 'loginID' in session:
        return '<h1>Hello, needLogin1!</h1>'
    else:
        return """
            <h1>Login</h1><a href="%s">Go To Login</a>
                """ % url_for('login', next=request.url)


@app.route('/needlogin2/')
def needLogin2():
    if 'loginID' in session:
        return '<h1>Hello, needLogin2!</h1>'
    else:
        return redirect(url_for('loginPage', next=request.full_path))


@app.route('/logout/')
def logout():
    if 'loginID' in session:
        session.pop('loginID')
    return redirect(url_for('welcome'))


@app.route('/hello')
@app.route('/say', endpoint='new')
def hello():
    return 'Hello Flask!'


@app.route('/user/', defaults={'name': '陌生人'})
@app.route('/user/<name>')
def welcome(name):
    res = '<h1>Hello, %s!</h1>' % name
    if 'loginID' in session:
        res += 'Authenticated'
    else:
        res += 'UnAuthenticated'
    return res


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
