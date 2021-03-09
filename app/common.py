from flask import request, flash, Markup
from flask_babel import _, lazy_gettext as _l

def check_browser():
    '''
    check user's browser
    '''
    if request.user_agent.browser != 'chrome':
        flash(Markup(_('''<p>Your browser is not Google Chrome. For improving operability, we strongly recommend installing it:</p><br><button class="btn btn-default" onclick="window.open('https://www.google.com/chrome/','_blank')">Link to Google</button>''')))
        
        
