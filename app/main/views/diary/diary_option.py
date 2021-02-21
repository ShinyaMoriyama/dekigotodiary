import datetime
from flask import redirect, url_for, render_template, request, g
from flask_login import current_user
from ... import main
from .... import db
from ...forms.forms import FreeDiaryForm
from ....models import Category, Diary

@main.route('/diary_option_new', methods=['GET', 'POST'])
def diary_option_new():
    form = FreeDiaryForm()

    args_category = int(request.args.get('optional_category'))
    optional_category_name = ''
    optional_category_template = ''
    for optional_category in g.optional_category_list:
        if optional_category[0] == args_category:
            optional_category_name = optional_category[1]
            optional_category_template = optional_category[3]
            break

    if form.validate_on_submit():
        date = form.date.data
        note = form.note.data
        diary = Diary(
            category=Category.OPTION,
            date=date,
            note=note,
            user=current_user._get_current_object(),
            optional_category=args_category,)

        db.session.add(diary)
        db.session.commit()

        return redirect(url_for('.index'))

    date = request.args.get('date')
    if date:
        form.date.data = datetime.datetime.strptime(date, '%Y-%m-%d')
    else:
        form.date.data = datetime.date.today()

    if optional_category_template:
        form.note.data = optional_category_template

    return render_template(
        'diary/diary_option_edit.html',
        form = form,
        is_edit = False,
        optional_category_name = optional_category_name,
    )

@main.route('/diary_option_edit/<id>', methods=['GET', 'POST'])
def diary_option_edit(id):
    form = FreeDiaryForm()

    data = Diary.query.get(id)
    data_category = data.optional_category

    optional_category_name = ''
    for optional_category in g.optional_category_list:
        if optional_category[0] == data_category:
            optional_category_name = optional_category[1]
            break

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
        'diary/diary_option_edit.html',
        form = form,
        is_edit = True,
        optional_category_name = optional_category_name,        
    )
