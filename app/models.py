from flask_login import UserMixin
from . import db, login_manager

class Diary(db.Model):
    __tablename__ = 'Diary'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    note = db.Column(db.Text)
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
