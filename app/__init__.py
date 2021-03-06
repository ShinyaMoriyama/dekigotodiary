import os
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.contrib.twitter import make_twitter_blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config

db = SQLAlchemy()
bootstrap = Bootstrap()

login_manager = LoginManager()
login_manager.login_view = '.login'

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    app.logger.info('FLASK_CONFIG %s', os.getenv('FLASK_CONFIG'))
    app.logger.info('FLASK_DEBUG %s', os.getenv('FLASK_DEBUG'))

    stripe_mode = 'LIVE!!' if app.config['STRIPE_LIVE'] == '1' else 'TEST'
    app.logger.info('@@@ Stripe mode @@@ is %s', stripe_mode)

    app.jinja_env.globals.update(len=len)

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    if app.config['SSL_REDIRECT']:
        from flask_sslify import SSLify
        sslify = SSLify(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # google
    google_blueprint = make_google_blueprint(
        scope=[
            "https://www.googleapis.com/auth/userinfo.email",
            "https://www.googleapis.com/auth/userinfo.profile",
            "openid",
            ],
        client_id=app.config['GOOGLE_CLIENT_ID'],
        client_secret=app.config['GOOGLE_CLIENT_SECRET'],
        )
    app.register_blueprint(google_blueprint, url_prefix="/login")

    # twitter
    twitter_blueprint = make_twitter_blueprint(
        api_key=app.config['TWITTER_API_KEY'],
        api_secret=app.config['TWITTER_API_SECRET'],
    )
    app.register_blueprint(twitter_blueprint, url_prefix="/login")

    # app.logger.info('url_map= %s', app.url_map)
    # app.logger.info('config= %s', app.config)

    return app

