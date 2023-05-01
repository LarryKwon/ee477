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

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import UniqueConstraint

builtin_list = list

db = SQLAlchemy()


def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)


def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data


# [START model]
class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    author = db.Column(db.String(255))
    publishedDate = db.Column(db.String(255))
    year = db.Column(db.Integer)
    imageUrl = db.Column(db.String(255))
    description = db.Column(db.String(4096))
    createdBy = db.Column(db.String(255))
    createdById = db.Column(db.String(255))

    def __repr__(self):
        return "<Book(title='%s', author=%s)" % (self.title, self.author)


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    is_active = db.Column(db.Boolean, default=True)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        print(self.is_active)
        return self.is_active

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id)
        except AttributeError:
            raise NotImplementedError("No `id` attribute - override `get_id`") from None

    def __init__(self, email, password):
        self.email = email
        self.password = password
        return self

    def __repr__(self):
        return "<User(email='%s', password=%s)" % (self.email, self.password)


class BookRate(db.Model):
    __tablename__ = 'bookRate'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    rate = db.Column(db.Integer, nullable=True)


# [END model]


# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Book.query
             .order_by(Book.title)
             .limit(limit)
             .offset(cursor))
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)


# [END list]


# [START read]
def read(id):
    result = Book.query.get(id)
    if not result:
        return None
    return from_sql(result)


def searchBooks(title, year, limit=10, cursor=None):
    if (title != '' and year != ''):
        query = Book.query.filter(Book.title == title, Book.year == year).order_by(Book.title).limit(limit).offset(
            cursor)
    elif (title == '' and year != ''):
        query = Book.query.filter(Book.year == year).order_by(Book.title).limit(limit).offset(
            cursor)
    elif (year == '' and title != ''):
        query = Book.query.filter(Book.title == title).order_by(Book.title).limit(limit).offset(
            cursor)
    else:
        query = Book.query.filter(Book.title == title, Book.year == year).order_by(Book.title).limit(limit).offset(
            cursor)
    books = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(books) == limit else None
    return (books, next_page)


def getUserInfo(user_email, user_pw):
    result = User.query.filter(User.email == user_email, User.password == user_pw).first()
    # print(result)
    if not result:
        return None
    return from_sql(result)


def getUserInfoById(userId):
    result = User.query.get(userId)
    print(result)
    if not result:
        return None
    return from_sql(result)


# [END read]


# [START create]
def create(data):
    book = Book(**data)
    db.session.add(book)
    db.session.commit()
    return from_sql(book)


def create_user(email, password):
    user = User(email, password)
    print(user)
    db.session.add(user)
    db.session.commit()
    return from_sql(user)


# [END create]


# [START update]
def update(data, id):
    book = Book.query.get(id)
    for k, v in data.items():
        setattr(book, k, v)
    db.session.commit()
    return from_sql(book)


# [END update]


def delete(id):
    Book.query.filter_by(id=id).delete()
    db.session.commit()


def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()
