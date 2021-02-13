import requests
import datetime
import json
from flask import redirect, url_for, render_template, current_app, flash, request
from flask_login import current_user
from wtforms.validators import URL, ValidationError
from bs4 import BeautifulSoup
from ... import main
from .... import db
from ...forms.forms import ReadDiaryForm
from ....models import Category, Diary

def scrape_amazon(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, features="lxml")
    if soup.select("#productTitle") is None or soup.select("#productTitle") == []:
        current_app.logger.info('#productTitle')
        return None, None
    title = soup.select("#productTitle")[0].get_text().strip()

    # paper
    img_div = soup.find(id="img-wrapper")
    if img_div is not None:
        imgs_str = img_div.img.get('data-a-dynamic-image')  # a string in Json format
        if imgs_str is not None:
            imgs_dict = json.loads(imgs_str)
            img_src = list(imgs_dict.keys())[0]
            return title, img_src

    # kindle
    img_div = soup.find(id="ebooks-img-wrapper")
    if img_div is not None:
        imgs_str = img_div.img.get('data-a-dynamic-image')  # a string in Json format
        if imgs_str is not None:
            imgs_dict = json.loads(imgs_str)
            img_src = list(imgs_dict.keys())[0]
            return title, img_src

    # audible
    img_div = soup.find(id="audibleimageblock_feature_div").find(id="main-image")
    if img_div is not None:
        img_src = img_div['src']
        if img_src is not None:
            return title, img_src
    
    return None, None

def process_get_title(form):
    # use case for deleting existing title and image
    if form.book_url.data == '':
        form.book_title.data = ''
        form.book_img_src.data = ''
        return render_template(
            'diary/diary_read_edit.html',
            form = form,
        )

    try:
        URL()(form, form.book_url)
    except ValidationError as ve:
        current_app.logger.info(ve)
        flash(ve)
        return render_template(
            'diary/diary_read_edit.html',
            form = form,
        )
    url = form.book_url.data
    title, img_src = scrape_amazon(url)
    current_app.logger.info('title= %s', title)
    current_app.logger.info('img_src= %s', img_src)
    
    form.book_title.data = title
    form.book_img_src.data = img_src

    return render_template(
        'diary/diary_read_edit.html',
        form = form,
    )

@main.route('/diary_read_new', methods=['GET', 'POST'])
def diary_read_new():
    form = ReadDiaryForm()

    if form.is_submitted() and form.get_info.data:
        rt = process_get_title(form)
        return rt

    if form.validate_on_submit():
        date = form.date.data
        book_url = form.book_url.data
        book_title = form.book_title.data
        book_img_src = form.book_img_src.data
        note = form.note.data
        diary = Diary(
            category=Category.READ,
            date=date,
            book_url = book_url,
            book_title = book_title,
            book_img_src = book_img_src,
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

    if form.is_submitted() and form.get_info.data:
        rt = process_get_title(form)
        return rt

    if form.is_submitted() and form.submit.data and form.validate_on_submit():
        data.date = form.date.data
        data.book_url = form.book_url.data
        data.book_title = form.book_title.data
        data.book_img_scr = form.book_img_src.data
        data.note = form.note.data
        db.session.commit()

        return redirect(url_for('.index'))

    if form.is_submitted() and form.delete.data:
        db.session.delete(data)
        db.session.commit()

        return redirect(url_for('.index'))

    form.date.data = data.date
    form.book_url.data = data.book_url
    form.book_title.data = data.book_title
    form.book_img_src.data = data.book_img_src
    form.note.data = data.note

    return render_template(
        'diary/diary_read_edit.html',
        form = form,
        is_edit = True,
    )
