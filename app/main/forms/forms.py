from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
    
class EditForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d')
    note = TextAreaField('Note')
    submit = SubmitField('Submit')