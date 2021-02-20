from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, IntegerField, StringField, HiddenField, BooleanField
from wtforms.fields.html5 import DateField, DateTimeLocalField, URLField
from wtforms.validators import DataRequired, NumberRange
from flask_babel import _, lazy_gettext as _l

class DiaryCommonForm(FlaskForm):
    category = SelectField(_l('Category'), choices=[
        ('', ''), (1, _l('Free Diary')), (2, _l('Sleep Diary')), (3, _l('Drinking Diary')), (4, _l('Reading Diary'))],
        default='')
    submit = SubmitField(_l('Submit'))

class FreeDiaryForm(FlaskForm):
    date = DateField(_l('Date'), format='%Y-%m-%d', validators=[DataRequired()])
    note = TextAreaField(_l('Note'))
    submit = SubmitField(_l('Submit'))
    delete = SubmitField(_l('Delete'))

class SleepDiaryForm(FlaskForm):
    allday = BooleanField(_l('All-day'))
    date = DateField(_l('Date'), format='%Y-%m-%d')
    start = DateTimeLocalField(_l('Start'), format='%Y-%m-%dT%H:%M')
    end = DateTimeLocalField(_l('End'), format='%Y-%m-%dT%H:%M')
    sleep_condition = SelectField(_l('Sleep Condition'), choices=[(0, 'NG'), (1, 'OK')], coerce=int, default=1)
    note = TextAreaField(_l('Note'))
    submit = SubmitField(_l('Submit'))
    delete = SubmitField(_l('Delete'))

class DrinkDiaryForm(FlaskForm):
    date = DateField(_l('Date'), format='%Y-%m-%d', validators=[DataRequired()])
    amt_of_drink = IntegerField(_l('The amount of pure alcohol (g)'), validators=[NumberRange(min=0, max=999)])
    note = TextAreaField(_l('Note'))
    submit = SubmitField(_l('Submit'))
    delete = SubmitField(_l('Delete'))

class ReadDiaryForm(FlaskForm):
    date = DateField(_l('Date'), format='%Y-%m-%d', validators=[DataRequired()])
    book_isbn = StringField('ISBN')
    get_info = SubmitField(_l('Book Info'))
    book_title = StringField(_l('Title'), validators=[DataRequired()])
    book_subtitle = StringField(_l('Subtitle'))
    book_img_src = HiddenField('Image Src')
    book_author = StringField(_l('Author'))
    book_url = HiddenField('book url')
    note = TextAreaField(_l('Note'))
    submit = SubmitField(_l('Submit'))
    delete = SubmitField(_l('Delete'))

class AccountForm(FlaskForm):
    submit = SubmitField(_l('Payment information (Stripe)'))
