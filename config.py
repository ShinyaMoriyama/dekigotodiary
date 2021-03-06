import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('CSRF_SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
    TWITTER_API_KEY = os.environ.get('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.environ.get('TWITTER_API_SECRET')
    SSL_REDIRECT = False
    BC_FREE = 'Tomato'
    BC_SLEEP = 'SeaGreen'
    BC_DRINK = 'MediumOrchid'
    BC_READ = 'RoyalBlue'
    LANGUAGES = ['en', 'ja']
    PERIOD_FREE_TRIAL = 60,

    STRIPE_LIVE = os.environ.get('STRIPE_LIVE')
    STRIPE_API_VERSION=os.environ.get('STRIPE_API_VERSION')
    if os.environ.get('STRIPE_LIVE') == '1':
        STRIPE_WEBHOOK_SECRET = os.environ.get('LIVE_STRIPE_WEBHOOK_SECRET')
        STRIPE_SECRET_KEY = os.environ.get('LIVE_STRIPE_SECRET_KEY')
        STRIPE_PUBLISHABLE_KEY = os.environ.get('LIVE_STRIPE_PUBLISHABLE_KEY')
        JPY_PRICE_ID = os.environ.get('LIVE_JPY_PRICE_ID')
        USD_PRICE_ID = os.environ.get('LIVE_USD_PRICE_ID')
        TAX_RATE_ID = os.environ.get('LIVE_TAX_RATE_ID')
    else:
        if os.environ.get('STRIPE_WEBHOOK_CLI') == '1':
            STRIPE_WEBHOOK_SECRET = os.environ.get('TEST_STRIPE_WEBHOOK_SECRET_CLI')
        else:
            STRIPE_WEBHOOK_SECRET = os.environ.get('TEST_STRIPE_WEBHOOK_SECRET')
        STRIPE_SECRET_KEY = os.environ.get('TEST_STRIPE_SECRET_KEY')
        STRIPE_PUBLISHABLE_KEY = os.environ.get('TEST_STRIPE_PUBLISHABLE_KEY')
        JPY_PRICE_ID = os.environ.get('TEST_JPY_PRICE_ID')
        USD_PRICE_ID = os.environ.get('TEST_USD_PRICE_ID')
        TAX_RATE_ID = os.environ.get('TEST_TAX_RATE_ID')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data-dev.sqlite')

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
        'sqlite://'

class HerokuConfig(Config):
    SSL_REDIRECT = True if os.environ.get('DYNO') else False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'data.sqlite')

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # handle reverse proxy server headers
        # from werkzeug.contrib.fixers import ProxyFix
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        app.logger.setLevel(logging.DEBUG) # change level from WARNING to DEBUG

        from flask import logging as flog
        flog.default_handler.setFormatter(logging.Formatter("%(levelname)s in %(module)s: %(message)s"))

        # from logging import StreamHandler
        # file_handler = StreamHandler()
        # file_handler.setLevel(logging.INFO)
        # formatter = logging.Formatter('%(levelname)s in %(module)s: %(message)s')
        # file_handler.setFormatter(formatter)
        # app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig
}
