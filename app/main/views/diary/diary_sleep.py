import datetime
from flask import redirect, url_for, render_template
from flask_login import current_user
from ... import main
from .... import db
from ...forms.forms import SleepDiaryForm
from ....models import Category, Diary

@main.route('/diary_sleep_new', methods=['GET', 'POST'])
def diary_sleep_new():
    form = SleepDiaryForm()

    if form.validate_on_submit():
        if form.allday.data == True:
            start = None
            end = None
            date = form.date.data
            sleep_time = None
        else:
            start = form.start.data
            end = form.end.data
            date = start.date()
            sleep_time = end - start
        sleep_condition = form.sleep_condition.data
        note = form.note.data
        diary = Diary(
            category=Category.SLEEP,
            start=start,
            end=end,
            date=date,
            sleep_time=sleep_time,
            sleep_condition=sleep_condition,
            note=note,
            user=current_user._get_current_object())

        db.session.add(diary)
        db.session.commit()

        return redirect(url_for('.index'))

    form.start.data = datetime.date.today() - datetime.timedelta(days=1)
    form.end.data = datetime.date.today()
    form.date.data = form.start.data

    return render_template(
        'diary/diary_sleep_edit.html',
        form = form,
        is_edit = False,
    )

@main.route('/diary_sleep_edit/<id>', methods=['GET', 'POST'])
def diary_sleep_edit(id):
    form = SleepDiaryForm()

    data = Diary.query.get(id)

    if form.is_submitted() and form.submit.data and form.validate_on_submit():
        if form.allday.data == True:
            start = None
            end = None
            date = form.date.data
            sleep_time = None
        else:
            start = form.start.data
            end = form.end.data
            date = start.date()
            sleep_time = end - start
        data.start = start
        data.end = end
        data.date = date
        data.sleep_time = sleep_time
        data.sleep_condition = form.sleep_condition.data
        data.note = form.note.data
        db.session.commit()

        return redirect(url_for('.index'))

    if form.is_submitted() and form.delete.data:
        db.session.delete(data)
        db.session.commit()

        return redirect(url_for('.index'))

    if data.end is None:
        form.allday.data = True
        form.start.data = data.date
        form.end.data = data.date + datetime.timedelta(days=1)
        form.date.data = data.date
    else:
        form.allday.data = False
        form.start.data = data.start
        form.end.data = data.end
        form.date.data = data.start
    form.sleep_condition.data = data.sleep_condition
    form.note.data = data.note

    return render_template(
        'diary/diary_sleep_edit.html',
        form = form,
        is_edit = True,
    )
