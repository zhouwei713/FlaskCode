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
from wtforms import StringField, PasswordField, FileField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail, Message
from threading import Thread


app = Flask(__name__)
app.secret_key = 'Very Hard Secret'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_PATH'] = os.path.join(app.root_path, 'uploads')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_USERNAME'] = 'mowuxue1989@163.com'
app.config['MAIL_PASSWORD'] = 'PJIKJQNZJJWDOLTA'
# app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
mail = Mail(app)


def send_email(to, subject, bogy):
    print(app.config['MAIL_PASSWORD'])
    print(app.config['MAIL_USERNAME'])
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to], body=bogy)
    mail.send(msg)


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship('User', backref='role')


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(4, 10)])
    submit = SubmitField('Login')


class UploadForm(FlaskForm):
    photo = FileField('Upload Image', validators=[file_required(), file_allowed(['png', 'jpg'])])
    submit = SubmitField('Upload')


class SendEmailForm(FlaskForm):
    emailAddress = StringField('Email Address', validators=[DataRequired()])
    message = TextAreaField()
    submit = SubmitField("Send")


@app.route('/sendemail', methods=['GET', 'POST'])
def sendemail():
    form = SendEmailForm()
    if form.validate_on_submit():
        eAddress = form.emailAddress.data
        message = form.message.data
        flash("Start Send Email!")
        send_email(eAddress, "My Email", message)
        return redirect(url_for('index'))
    return render_template('email.html', form=form)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email_saync(to, subject, body):
    msg = Message(subject, sender=app.config['MAIL_USERNAME'], recipients=[to], body=body)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = f.filename
        f.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        flash('Upload file successful!')
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
        user = User(username=username)
        db.session.add(user)
        db.session.commit()
        flash("Login Successful!")
        return redirect(url_for('index'))
    return render_template('login.html', form=form)


@app.route('/')
def index():
    user = session.get('username')
    isUser = User.query.filter_by(username=user).first()
    if isUser is None:
        session['known'] = False
    else:
        session['known'] = True
    return render_template('index.html', user=user, known=session.get('known', False))


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


@app.route('/user/', defaults={'name': 'No User'})
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
