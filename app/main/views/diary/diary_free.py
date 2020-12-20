import datetime
from flask import redirect, url_for, render_template
from flask_login import current_user
from ... import main
from .... import db
from ...forms.forms import FreeDiaryForm
from ....models import Category, Diary

@main.route('/diary_free_new', methods=['GET', 'POST'])
def diary_free_new():
    form = FreeDiaryForm()

    if form.validate_on_submit():
        date = form.date.data
        note = form.note.data
        diary = Diary(
            category=Category.FREE,
            date=date,
            note=note,
            user=current_user._get_current_object())

        db.session.add(diary)
        db.session.commit()

        return redirect(url_for('.index'))

    form.date.data = datetime.date.today()

    return render_template(
        'diary/diary_free_edit.html',
        form = form,
        is_edit = False,
    )

@main.route('/diary_free_edit/<id>', methods=['GET', 'POST'])
def diary_free_edit(id):
    form = FreeDiaryForm()

    data = Diary.query.get(id)

    if form.is_submitted() and form.submit.data and form.validate_on_submit():
        data.date = form.date.data
        data.note = form.note.data
        db.session.commit()

        return redirect(url_for('.index'))

    if form.is_submitted() and form.delete.data:
        db.session.delete(data)
        db.session.commit()

        return redirect(url_for('.index'))

    form.date.data = data.date
    form.note.data = data.note

    return render_template(
        'diary/diary_free_edit.html',
        form = form,
        is_edit = True,
    )
