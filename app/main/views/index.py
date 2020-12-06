from oauthlib.oauth2.rfc6749.errors import InvalidGrantError, TokenExpiredError
from flask import render_template, redirect, url_for, current_app, session, request
from flask_dance.contrib.google import google
from flask_dance.contrib.twitter import twitter
from flask_login import current_user, login_user, logout_user

from datetime import datetime
from ..forms.forms import EditForm
from .. import main
from ...models import Diary, User
from ... import db
from pprint import pprint

@main.route('/', methods=['GET', 'POST'])
def index():
    diary_list = Diary.query.all()
    event_list = create_events(diary_list)
    
    print('current_user.is_authenticated: ', current_user.is_authenticated)
    print('current_user.is_anonymous: ', current_user.is_anonymous)
    print('current_user.get_id: ', current_user.get_id)
    print('current_user.is_active: ', current_user.is_active)
    print('session :', session)
    return render_template(
        'index.html',
        event_list=event_list,
    )

@main.route('/login', methods=['GET'])
def login():
    return render_template(
        'login.html',
    )

@main.route('/logout', methods=['GET', 'POST'])
def logout():

    if google.authorized:
        token = current_app.blueprints['google'].token["access_token"]
        print('session before deleting :', session)
        resp = google.post(
            "https://accounts.google.com/o/oauth2/revoke",
            params={"token": token},
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        del session['google_oauth_token']
        print('session after deleting :', session)
    elif twitter.authorized:
        token = current_app.blueprints['twitter'].token['oauth_token']
        print('session before deleting :', session)
        resp = twitter.post(
            "https://api.twitter.com/1.1/oauth/invalidate_token",
            params={"token": token},
        )
        del session['twitter_oauth_token']
        print('session after deleting twitter token:', session)
    
    logout_user()
    
    return render_template(
        'login.html',
    )

@main.route('/edit', methods=['GET', 'POST'])
def edit():
    print('current_user: ', current_user)
    print('current_user.is_authenticated: ', current_user.is_authenticated)
    print('current_user.is_anonymous: ', current_user.is_anonymous)
    print('current_user.get_id: ', current_user.get_id)
    print('current_user.is_active: ', current_user.is_active)
        
    form = EditForm()
    if form.is_submitted():
        date = form.date.data
        note = form.note.data
        diary = Diary(date=date, note=note)

        db.session.add(diary)
        db.session.commit()

        return redirect(url_for('.index'))

    return render_template(
        'edit.html',
        form = form,
    )

@main.route('/edit/<id>', methods=['GET', 'POST'])
def edit_id(id):
    form = EditForm()

    data = Diary.query.get(id)

    if form.is_submitted():
        data.date = form.date.data
        data.note = form.note.data
        db.session.commit()

        return redirect(url_for('.index'))

    form.date.data = data.date
    form.note.data = data.note

    return render_template(
        'edit.html',
        form = form,
    )


def row2dict(row):
    '''
    from Stackoverflow for future reference
    '''
    d = {}
    for column in row.__table__.columns:
        d[column.name] = str(getattr(row, column.name))

    return d

def create_events(diary_list):
    return [ diary2event(diary) for diary in diary_list ]

def diary2event(diary):
    d = {}
    d['title'] = diary.note
    d['start'] = diary.date.strftime('%Y-%m-%d')
    d['url'] = 'edit/' + str(diary.id)
    return d

from flask_dance.consumer import oauth_authorized

@oauth_authorized.connect
def logged_in(blueprint, token):
    '''
    triggered after logging in with SNS via OAuth
    '''
    print('@@@@logged_in@@@@: ', blueprint.name.capitalize())
    print('@@@@token@@@@: ', token)
    if google.authorized:
        # workaround by https://github.com/singingwolfboy/flask-dance/issues/35
        try:
            account_info = google.get('/oauth2/v1/userinfo')
        except (InvalidGrantError, TokenExpiredError) as e:
            return redirect(url_for("google.login"))
        if account_info.ok:
            account_info_json = account_info.json()
            print('@@@@email: ', account_info_json['email'])
            print('@@@@account_info: ', account_info_json)
            print('@@@@access_token: ', current_app.blueprints['google'].token) # can not get .token["access_token"] at the time
    elif twitter.authorized:
        account_info = twitter.get("account/verify_credentials.json")
        if account_info.ok:
            account_info_json = account_info.json()
            print('@@@@screen_name: ', account_info_json['screen_name'])
            print('@@@@account_info: ', account_info_json)
            print('@@@@oauth_token: ', current_app.blueprints['twitter'].token) # can not get .token['oauth_token'] at the time
    user = User.query.filter_by(account_id=account_info_json['id']).first()
    print('######account_info: ', type(account_info_json))
    if user is None:
        user_add = User(
            account_id=account_info_json['id'],
            account_info=account_info_json,
            last_login=datetime.now())
        db.session.add(user_add)
        db.session.commit()
        login_user(user_add, remember=True)
    else:
        user.account_info=account_info_json
        user.last_login=datetime.now()
        db.session.commit()
        login_user(user, remember=True)

@main.before_app_request
def before_request():
    '''
    triggered before executing all view functions
    '''
    print('@@@@request.endpoint@@@@: ', request.endpoint)
    print('@@@@session@@@@: ', session)
    # print('@@@@app_context: ', current_app._get_current_object().__dict__)
    if request.endpoint in [
        'static',
        'main.login',
        'main.logout',
        'google.login',
        'twitter.login',
        'google.authorized',
        'twitter.authorized',
        ]:
        return
    if current_user.is_authenticated:
    # if google.authorized or twitter.authorized:
        return
    return redirect(url_for('main.login'))
