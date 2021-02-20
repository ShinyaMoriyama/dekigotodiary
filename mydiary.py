import os
import click
from flask import request
from flask_migrate import Migrate, upgrade
from flask_babel import Babel
from app import create_app, db
from app.models import Diary, User
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(app, db, render_as_batch=True)
babel = Babel(app)

@babel.localeselector
def get_locale():
    return request.accept_languages.best_match(app.config['LANGUAGES'])

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Diary=Diary, User=User)

@app.cli.command()
def deploy():
    """Run deployment tasks."""
    # migrate database to latest revision
    upgrade()

@app.cli.group()
def translate():
    """Translation and localization commands."""
    pass

@translate.command()
def update():
    """Update all languages."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system('pybabel update -i messages.pot -d app/translations'):
        raise RuntimeError('update command failed')
    os.remove('messages.pot')

@translate.command()
def compile():
    """Compile all languages."""
    if os.system('pybabel compile -d app/translations'):
        raise RuntimeError('compile command failed')

@translate.command()
@click.argument('lang')
def init(lang):
    """Initialize a new language."""
    if os.system('pybabel extract -F babel.cfg -k _l -o messages.pot .'):
        raise RuntimeError('extract command failed')
    if os.system(
            'pybabel init -i messages.pot -d app/translations -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove('messages.pot')