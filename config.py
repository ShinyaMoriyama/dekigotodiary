import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
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

    # Stripe keys
    STRIPE_API_VERSION='2020-08-27'
    STRIPE_PUBLISHABLE_KEY='pk_test_51IAtx3DiY6soNfkvKoMpJzdUUk2x95EeuqdMvn9jFxPvHN0Fb9SUrwWV3bdSlAGNi3voY3JwIzZGuyhx7ZVGg7US00fRs4FMNB'
    STRIPE_SECRET_KEY='sk_test_51IAtx3DiY6soNfkvT2rglxj8lfGI9fjW7JomMVwpXoNVeOl63euxjdbXjq7XrH6waUfk1GEuya3SXaIbjYVoDc3G00zhIfqasX'

    # Required to run webhook
    # See README on how to use the Stripe CLI to setup
    STRIPE_WEBHOOK_SECRET=os.environ.get('STRIPE_WEBHOOK_SECRET') or 'whsec_sm04TvOznnMo594Qqiajju1wf55XGDrw'
                           
    # Stripe subscription data
    JPY_PRICE_ID='price_1IBRRXDiY6soNfkvvbWBOI3e'
    USD_PRICE_ID='price_1IBRRXDiY6soNfkvk4YwoI6n'
    TAX_RATE_ID='txr_1ICBo5DiY6soNfkvIVjzJK1I'

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
    STRIPE_WEBHOOK_SECRET='whsec_sm04TvOznnMo594Qqiajju1wf55XGDrw' # override

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # handle reverse proxy server headers
        # from werkzeug.contrib.fixers import ProxyFix
        from werkzeug.middleware.proxy_fix import ProxyFix
        app.wsgi_app = ProxyFix(app.wsgi_app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'heroku': HerokuConfig,

    'default': DevelopmentConfig
}
