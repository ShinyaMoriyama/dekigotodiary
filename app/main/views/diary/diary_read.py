import requests
import datetime
from flask import redirect, url_for, render_template, current_app, request, flash
from flask_login import current_user
from flask_babel import _, lazy_gettext as _l
from ... import main
from .... import db
from ...forms.forms import ReadDiaryForm
from ....models import Category, Diary

def process_get_book_info(form):
    isbn = form.book_isbn.data
    isbn = isbn.replace('-', '')
    google_books_api_url = 'https://www.googleapis.com/books/v1/volumes?q=' + str(isbn) + '+isbn'
    r = requests.get(google_books_api_url)
    
    if r.status_code == requests.codes.ok and 'totalItems' in r.json() and r.json()['totalItems'] != 0:
        info = r.json()['items'][0]['volumeInfo']
        
        if 'title' in info:
            form.book_title.data = info['title']
        if 'subtitle' in info:
            form.book_subtitle.data = info['subtitle']
        if 'imageLinks' in info:
            if 'thumbnail' in info['imageLinks']:
                form.book_img_src.data = info['imageLinks']['thumbnail']
            else:
                form.book_img_src.data = list(info['imageLinks'].values())[0]
        if 'authors' in info:
            form.book_author.data = str(info['authors']).replace("'", '').replace('[', '').replace(']', '')
        if 'previewLink' in info:
            form.book_url.data = info['previewLink']
    else:
        flash(_('Can not get book info. Confirm the input and try again.'))

@main.route('/diary_read_new', methods=['GET', 'POST'])
def diary_read_new():
    form = ReadDiaryForm()

    if form.is_submitted() and form.get_info.data:
        process_get_book_info(form)
        return render_template(
            'diary/diary_read_edit.html',
            form = form,
            is_edit = False,
        )

    if form.validate_on_submit():
        date = form.date.data
        book_isbn = form.book_isbn.data
        book_title = form.book_title.data
        book_subtitle = form.book_subtitle.data
        book_img_src = form.book_img_src.data
        book_author = form.book_author.data
        book_url = form.book_url.data
        note = form.note.data
        diary = Diary(
            category=Category.READ,
            date=date,
            book_isbn = book_isbn,
            book_title = book_title,
            book_subtitle = book_subtitle,
            book_img_src = book_img_src,
            book_author = book_author,
            book_url = book_url,
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
        'diary/diary_read_edit.html',
        form = form,
        is_edit = False,
    )

@main.route('/diary_read_edit/<id>', methods=['GET', 'POST'])
def diary_read_edit(id):
    form = ReadDiaryForm()

    data = Diary.query.get(id)

    if form.is_submitted() and form.get_info.data and form.book_isbn.data != '':
        process_get_book_info(form)
        return render_template(
            'diary/diary_read_edit.html',
            form = form,
            is_edit = True,
        )

    if form.is_submitted() and form.submit.data and form.validate_on_submit():
        data.date = form.date.data
        data.book_isbn = form.book_isbn.data
        data.book_title = form.book_title.data
        data.book_subtitle = form.book_subtitle.data
        data.book_img_src = form.book_img_src.data
        data.book_author = form.book_author.data
        data.book_url = form.book_url.data
        data.note = form.note.data
        db.session.commit()

        return redirect(url_for('.index'))

    if form.is_submitted() and form.delete.data:
        db.session.delete(data)
        db.session.commit()

        return redirect(url_for('.index'))

    form.date.data = data.date
    form.book_isbn.data = data.book_isbn
    form.book_title.data = data.book_title
    form.book_subtitle.data = data.book_subtitle
    form.book_img_src.data = data.book_img_src
    form.book_author.data = data.book_author
    form.book_url.data = data.book_url
    form.note.data = data.note

    return render_template(
        'diary/diary_read_edit.html',
        form = form,
        is_edit = True,
    )
