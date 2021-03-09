import datetime
from flask import redirect, url_for, render_template, request
from flask_login import current_user
from ... import main
from ....common import check_browser
from .... import db
from ...forms.forms import DrinkDiaryForm
from ....models import Category, Diary

@main.route('/diary_drink_new', methods=['GET', 'POST'])
def diary_drink_new():
    form = DrinkDiaryForm()
    check_browser()

    if form.validate_on_submit():
        date = form.date.data
        amt_of_drink = form.amt_of_drink.data
        note = form.note.data
        diary = Diary(
            category=Category.DRINK,
            date=date,
            amt_of_drink=amt_of_drink,
            note=note,
            user=current_user._get_current_object())

        db.session.add(diary)
        db.session.commit()

        return redirect(url_for('.index'))

    date = request.args.get('date')
    if date:
        form.date.data = datetime.datetime.strptime(date, '%Y-%m-%d')
    else:
        form.date.data = datetime.date.today()
            
    return render_template(
        'diary/diary_drink_edit.html',
        form = form,
        is_edit = False,
    )

@main.route('/diary_drink_edit/<id>', methods=['GET', 'POST'])
def diary_drink_edit(id):
    form = DrinkDiaryForm()
    check_browser()

    data = Diary.query.get(id)

    if form.is_submitted() and form.submit.data and form.validate_on_submit():
        data.date = form.date.data
        data.amt_of_drink = form.amt_of_drink.data
        data.note = form.note.data
        db.session.commit()

        return redirect(url_for('.index'))

    if form.is_submitted() and form.delete.data:
        db.session.delete(data)
        db.session.commit()

        return redirect(url_for('.index'))

    form.date.data = data.date
    form.amt_of_drink.data = data.amt_of_drink
    form.note.data = data.note

    return render_template(
        'diary/diary_drink_edit.html',
        form = form,
        is_edit = True,
    )
