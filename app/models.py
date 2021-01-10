from flask_login import UserMixin
from . import db, login_manager

class Category:
    FREE = 1
    SLEEP = 2
    DRINK = 3
    READ = 4

class SleepCondition:
    OK = 1
    NG = 0

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
    book_title = db.Column(db.String(256))
    book_url = db.Column(db.String(1024))
    book_img_src = db.Column(db.String(1024))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))

class Provider:
    GOOGLE = 1
    TWITTER = 2

class User(UserMixin, db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.String(64), unique=True, index=True)
    account_info = db.Column(db.Text)
    last_login = db.Column(db.DateTime)
    diary = db.relationship('Diary', backref='user')

@login_manager.user_loader
def load_user(user_id):
    if user_id is None or user_id == 'None': 
        user_id='-1'
    return User.query.get(int(user_id))
