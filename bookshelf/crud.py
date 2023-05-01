# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask_login import current_user, login_required

from bookshelf import get_model
from flask import Blueprint, redirect, render_template, request, url_for

crud = Blueprint('crud', __name__)


# [START list]
@crud.route("/")
# @login_required
def list():
    if not current_user.is_authenticated:
        return redirect('/auth/login')
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    books, next_page_token = get_model().list(cursor=token)

    return render_template(
        "list.html",
        books=books,
        next_page_token=next_page_token)


# [END list]


@crud.route('/<id>')
@login_required
def view(id):
    if not current_user.is_authenticated:
        return redirect('/auth/login')
    book = get_model().read(id)
    rate = get_model().count_rate(id)
    myRate = get_model().get_book_rate(current_user.id, id)
    print(rate)
    return render_template("view.html", book=book,rate=rate,myRate=myRate)


@crud.route('/search', methods=['GET'])
def search():
    title = request.args['title']
    year = request.args['year']
    token = request.args.get('page_token', None)
    if token:
        token = token.encode('utf-8')

    if (title == '' and year == ''):
        return redirect('/books/')
    else:
        books, next_page_token = get_model().searchBooks(title, year, cursor=token)
    return render_template("list.html", books=books, next_page_token=next_page_token)


# [START add]
@crud.route('/add', methods=['GET', 'POST'])
# @login_required
def add():
    if not current_user.is_authenticated:
        return redirect('/auth/login')
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        book = get_model().create(data)

        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Add", book={})


# [END add]


@crud.route('/<id>/edit', methods=['GET', 'POST'])
# @login_required
def edit(id):
    if not current_user.is_authenticated:
        return redirect('/auth/login')
    book = get_model().read(id)

    if request.method == 'POST':
        data = request.form.to_dict(flat=True)
        book = get_model().update(data, id)
        return redirect(url_for('.view', id=book['id']))

    return render_template("form.html", action="Edit", book=book)


@crud.route('/<id>/delete')
def delete(id):
    if not current_user.is_authenticated:
        return redirect('/auth/login')
    get_model().delete(id)
    return redirect(url_for('.list'))


@crud.route('/<id>/rate', methods=['POST'])
def rate(id):
    if not current_user.is_authenticated:
        return redirect('/auth/login')
    try:
        rate = int(request.form.get('rating'))
        bookRate = get_model().get_book_rate(current_user.id, id)
        if bookRate:
            get_model().update_rate(current_user.id,id, rate)
        else:
            get_model().rate_books(current_user.id, id, rate)
        return redirect(url_for('.view', id=id))
    except ValueError:
        rate = None
        return redirect(url_for('.view', id=id))

