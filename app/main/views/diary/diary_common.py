import datetime
from flask import redirect, url_for, render_template
from ... import main
from ...forms.forms import DiaryCommonForm
from ....models import Category

@main.route('/diary_common/<date>', methods=['GET', 'POST'])
def diary_common(date):
    form = DiaryCommonForm()

    if form.is_submitted():
        category = form.category.data
        category = int(category) if category != '' else category

        if category == Category.FREE:
            return redirect(url_for('.diary_free_new', date=date))
        elif category == Category.SLEEP:
            return redirect(url_for('.diary_sleep_new', date=date))
        elif category == Category.DRINK:
            return redirect(url_for('.diary_drink_new', date=date))
        elif category == Category.READ:
            return redirect(url_for('.diary_read_new', date=date))

    return render_template(
        'diary/diary_common.html',
        form = form,
    )
