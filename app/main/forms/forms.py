from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, IntegerField, StringField, HiddenField
from wtforms.fields.html5 import DateField, DateTimeLocalField, URLField
from wtforms.validators import DataRequired, URL

class DiaryCommonForm(FlaskForm):
    category = SelectField('Category', choices=[
        ('', ''), (1, 'Free Diary'), (2, 'Sleep Diary'), (3, 'Drinking Diary'), (4, 'Reading Diary')])
    submit = SubmitField('Submit')

class FreeDiaryForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    note = TextAreaField('Note')
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

class SleepDiaryForm(FlaskForm):
    start = DateTimeLocalField('Start', format='%Y-%m-%dT%H:%M')
    end = DateTimeLocalField('End', format='%Y-%m-%dT%H:%M')
    sleep_condition = SelectField('Sleep Condition', choices=[(0, 'OK'), (1, 'NG')])
    note = TextAreaField('Note')
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

class DrinkDiaryForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    amt_of_drink = IntegerField('The amount of pure alcohol (g)', validators=[DataRequired()])
    note = TextAreaField('Note')
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')

class ReadDiaryForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    book_url = URLField('URL')
    get_info = SubmitField('Get Title')
    book_title = StringField('Title', validators=[DataRequired()])
    book_img_src = HiddenField('Image Src')
    note = TextAreaField('Note')
    submit = SubmitField('Submit')
    delete = SubmitField('Delete')
