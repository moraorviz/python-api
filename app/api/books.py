'''
Created on Nov 25, 2018

@author: mario
'''

from flask import jsonify, request, g, url_for, current_app
from . import api
from ..models import Book
from .. import db


@api.route('/books')
def get_books():
    print('Consultando libros')
    books = Book.query.all()
    resultList = []
    for book in books:
        resultList.append(jsonify(book))
    return resultList
    

@api.route('/books/<int:id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_jsonld())


@api.route('/books/', methods=['POST'])
def new_book():
    book = Book.from_json(request.json)
    db.session.add(book)
    db.session.commit()
    return jsonify(book.to_json()), 201, \
        {'Location': url_for('api.get_book', id=book.id)}




