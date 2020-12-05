from flask import render_template, redirect, url_for, current_app, session
from flask_dance.contrib.google import google
from flask_dance.contrib.twitter import twitter
from .. import main
from pprint import pprint

@main.route('/calendar', methods=['GET', 'POST'])
def calendar():

    return render_template(
        'calendar.html',
    )
