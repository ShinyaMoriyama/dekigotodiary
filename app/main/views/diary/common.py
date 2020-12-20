from flask import redirect, url_for, render_template
from ... import main
from ...forms.forms import DiaryCommonForm
from ....models import Category

@main.route('/diary_common', methods=['GET', 'POST'])
def diary_common():
    form = DiaryCommonForm()

    if form.is_submitted():
        category = form.category.data
        category = int(category) if category != '' else category

        if category == Category.FREE:
            return redirect(url_for('.free_diary_new'))
        elif category == Category.SLEEP:
            return redirect(url_for('.sleep_diary_new'))
        elif category == Category.DRINK:
            return redirect(url_for('.drink_diary_new'))
        elif category == Category.READ:
            return redirect(url_for('.read_diary_new'))

    return render_template(
        'diary/diary_common.html',
        form = form,
    )
