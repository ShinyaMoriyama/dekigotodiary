from flask import redirect, url_for, render_template
from flask_login import current_user
from ... import main
from ...forms.forms import DiaryCommonForm
from ....models import Category, OptionalCategory

@main.route('/diary_common/<date>', methods=['GET', 'POST'])
def diary_common(date):
    form = DiaryCommonForm()
    query_result_list = OptionalCategory.query.filter_by(
        user=current_user._get_current_object()).order_by(
            OptionalCategory.optional_category.asc()).all()
    optional_category_list = [(cate.optional_category, cate.name) for cate in query_result_list ]
    form.category.choices += optional_category_list

    if form.is_submitted() and form.category.data != '':
        category = form.category.data
        category = int(category)

        if category == Category.FREE:
            return redirect(url_for('.diary_free_new', date=date))
        elif category == Category.SLEEP:
            return redirect(url_for('.diary_sleep_new', date=date))
        elif category == Category.DRINK:
            return redirect(url_for('.diary_drink_new', date=date))
        elif category == Category.READ:
            return redirect(url_for('.diary_read_new', date=date))
        else:
            return redirect(
                url_for('.diary_option_new', date=date, optional_category=category))

    return render_template(
        'diary/diary_common.html',
        form = form,
    )
