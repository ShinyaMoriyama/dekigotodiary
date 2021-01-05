from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, IntegerField, StringField, HiddenField
from wtforms.fields.html5 import DateField, DateTimeLocalField, URLField
from wtforms.validators import DataRequired
from flask_babel import _, lazy_gettext as _l

class DiaryCommonForm(FlaskForm):
    category = SelectField(_l('Category'), choices=[
        ('', ''), (1, _l('Free Diary')), (2, _l('Sleep Diary')), (3, _l('Drinking Diary')), (4, _l('Reading Diary'))])
    submit = SubmitField(_l('Submit'))

class FreeDiaryForm(FlaskForm):
    date = DateField(_l('Date'), format='%Y-%m-%d', validators=[DataRequired()])
    note = TextAreaField(_l('Note'))
    submit = SubmitField(_l('Submit'))
    delete = SubmitField(_l('Delete'))

class SleepDiaryForm(FlaskForm):
    start = DateTimeLocalField(_l('Start'), format='%Y-%m-%dT%H:%M')
    end = DateTimeLocalField(_l('End'), format='%Y-%m-%dT%H:%M')
    sleep_condition = SelectField(_l('Sleep Condition'), choices=[(0, 'OK'), (1, 'NG')])
    note = TextAreaField(_l('Note'))
    submit = SubmitField(_l('Submit'))
    delete = SubmitField(_l('Delete'))

class DrinkDiaryForm(FlaskForm):
    date = DateField(_l('Date'), format='%Y-%m-%d', validators=[DataRequired()])
    amt_of_drink = IntegerField(_l('The amount of pure alcohol (g)'), validators=[DataRequired()])
    note = TextAreaField(_l('Note'))
    submit = SubmitField(_l('Submit'))
    delete = SubmitField(_l('Delete'))

class ReadDiaryForm(FlaskForm):
    date = DateField(_l('Date'), format='%Y-%m-%d', validators=[DataRequired()])
    book_url = URLField('URL')
    get_info = SubmitField(_l('Get Title'))
    book_title = StringField(_l('Title'), validators=[DataRequired()])
    book_img_src = HiddenField('Image Src')
    note = TextAreaField(_l('Note'))
    submit = SubmitField(_l('Submit'))
    delete = SubmitField(_l('Delete'))
