from re import template
from flask_login import UserMixin
from . import db, login_manager

class Category:
    FREE = 1
    SLEEP = 2
    DRINK = 3
    READ = 4
    OPTION = 9

class SleepCondition:
    NG = 0
    OK = 1

class DrinkCondition:
    NOTBAD = 0
    HUNGOVER = 1

class Diary(db.Model):
    __tablename__ = 'Diary'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Integer)
    date = db.Column(db.Date)
    note = db.Column(db.Text)
    start = db.Column(db.DateTime)
    end = db.Column(db.DateTime)
    sleep_time = db.Column(db.Interval)
    sleep_condition = db.Column(db.Integer)
    amt_of_drink = db.Column(db.Integer)
    drink_condition = db.Column(db.Integer)
    book_isbn = db.Column(db.String(32))
    book_title = db.Column(db.String(256))
    book_subtitle = db.Column(db.String(256))
    book_img_src = db.Column(db.String(1024))
    book_author = db.Column(db.String(256))
    book_url = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    optional_category = db.Column(db.Integer)

class Provider:
    GOOGLE = 1
    TWITTER = 2

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(64), unique=True, index=True)
    account_provider = db.Column(db.Integer)
    account_info = db.Column(db.Text)
    first_login = db.Column(db.DateTime)
    last_login = db.Column(db.DateTime)
    stripe_customer = db.Column(db.String(64))
    stripe_status = db.Column(db.String(32))
    diary = db.relationship('Diary', backref='user')
    optional_category = db.relationship('OptionalCategory', backref='user')

class OptionalCategory(db.Model):
    __tablename__ = 'OptionalCategory'
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    optional_category = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    color = db.Column(db.String(12))
    template = db.Column(db.Text)

@login_manager.user_loader
def load_user(user_id):
    if user_id is None or user_id == 'None': 
        user_id='-1'
    return User.query.get(int(user_id))
