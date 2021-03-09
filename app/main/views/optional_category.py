from flask import redirect, url_for, render_template
from flask_login import current_user
from .. import main
from ... import db
from ...common import check_browser
from ..forms.forms import OptionalCategoryForm
from ...models import Diary, OptionalCategory

@main.route('/optional_category_list', methods=['GET', 'POST'])
def optional_category_list():
    form = OptionalCategoryForm()

    if form.is_submitted() and form.add.data:
        return redirect(url_for('.optional_category_new'))

    return render_template(
        'optional_category_list.html',
        form=form)

@main.route('/optional_category_new', methods=['GET', 'POST'])
def optional_category_new():
    form = OptionalCategoryForm()
    check_browser()

    query = OptionalCategory.query.filter_by(
        user=current_user._get_current_object())
    count_for_check = len(query.all())

    if count_for_check > 0:
        max_cate = query.order_by(
            OptionalCategory.optional_category.desc()
            ).first().optional_category
    else:
        max_cate = 9 # Optional category starts 10 not to mix with original categories

    if form.is_submitted() and form.submit.data and form.validate_on_submit():
        name = form.name.data
        color = str(form.color.data)
        template = form.template.data
        optional_category = OptionalCategory(
            user=current_user._get_current_object(),
            optional_category=max_cate + 1,
            name=name,
            color=color,
            template=template,
            )

        db.session.add(optional_category)
        db.session.commit()

        return redirect(url_for('.optional_category_list'))

    return render_template(
        'optional_category_edit.html',
        form = form,
        is_edit = False,
    )

@main.route('/optional_category_edit/<id>', methods=['GET', 'POST'])
def optional_category_edit(id):
    form = OptionalCategoryForm()
    check_browser()

    record = OptionalCategory.query.get((current_user._get_current_object().id, int(id)))

    if form.is_submitted() and form.submit.data and form.validate_on_submit():
        record.name = form.name.data
        record.color = str(form.color.data)
        record.template = form.template.data
        db.session.commit()

        return redirect(url_for('.optional_category_list'))

    if form.is_submitted() and form.delete.data:
        diaries = Diary.query.filter_by(
            user_id=current_user.id, optional_category=int(id)).delete()
        db.session.delete(record)
        db.session.commit()

        return redirect(url_for('.optional_category_list'))

    form.name.data = record.name
    form.color.data = record.color
    form.template.data = record.template

    return render_template(
        'optional_category_edit.html',
        form = form,
        is_edit = True,
    )
