# coding = utf-8
"""
@author: zhou
@time:2019/11/5 11:13
@File: app.py
"""

from flask import Flask, url_for, request, session, redirect, render_template, flash, send_from_directory
from urllib.parse import urlparse
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from flask_wtf.file import file_required, file_allowed
from wtforms import StringField, PasswordField, FileField, SubmitField
from wtforms.validators import DataRequired, Length
import os


app = Flask(__name__)
app.secret_key = 'Very Hard Secret'
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
bootstrap = Bootstrap(app)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 10)])
    submit = SubmitField('Login')


class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[file_required(), file_allowed(['png', 'jpg'])])
    submit = SubmitField('Upload')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = f.filename
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('上传图片文件成功！')
        session['filename'] = filename
        return redirect(url_for('show_images'))
    return render_template('upload.html', form=form)


@app.route('/uploads/<path:filename>')
def get_file(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/uploaded-images')
def show_images():
    return render_template('uploaded.html')


def check_next(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(target)
    return ref_url.netloc == test_url.netloc


@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        session['username'] = username
        flash("登录成功，%s！" % username)
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/')
def index():
    user = session.get('username')
    return render_template('index.html', user=user)


@app.route('/needlogin1/')
def needLogin1():
    if 'loginID' in session:
        user = 'needLogin1'
        return render_template('hello.html', user=user)
    else:
        return render_template('needlogin.html')


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
