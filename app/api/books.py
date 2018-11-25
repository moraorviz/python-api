'''
Created on Nov 25, 2018

@author: mario
'''

from flask import jsonify, request, g, url_for, current_app
from . import api
from ..models import Book
from .. import db
import json

@api.route('/book')
def get_books():
    print('Consultando libros')
    books = Book.query.all()
    json_string = json.dumps([book.to_jsonld() for book in books])
    return json_string

@api.route('/book/<int:id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_jsonld())


@api.route('/book', methods=['POST'])
def new_book():
    book = Book.from_jsonld(request.json)
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_jsonld()), 201, \
        {'Location': url_for('api.get_book', id=book.id)}




