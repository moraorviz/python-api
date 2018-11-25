'''
Created on Nov 24, 2018

@author: mario
'''

from . import db
from flask import current_app, request, url_for
from datetime import datetime
from app.exceptions import ValidationError


class Thing:
    def __init__(self, nombre):
        self.nombre = nombre

class Person(Thing):
    def __init__(self, nombre, apellidos):
        super(Person, self).__init__(nombre)
        self.apellidos = apellidos

class CreativeWork(Thing):
        
        def __init__(self, nombre, autor, fechapub):
            super(CreativeWork, self).__init__(nombre)
            self.autor = autor
            self.fechapub = fechapub
    
class Book(db.Model, CreativeWork):
    __tablename__ = 'libros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True)
    autor = db.Column(db.String(64))
    fechapub = db.Column(db.Date)
    isbn = db.Column(db.String(64), unique=True)
    
    def __init__(self, **kwargs):
        super(Book, self).__init__(**kwargs)
    
    def add_isbn(self, isbn):
        self.isbn = isbn
        
    def __repr__(self):
        return '<User %r>' % self.nombre
    
    def to_jsonld(self):
        jsonld_post = {
            'url': url_for('api.get_book', id=self.id),
            '@context': 'http://schema.org',
            '@type': 'Book',
            'name': self.nombre,
            'author': {
                '@type': 'Person',
                'name': self.autor
            },
            'datePublished': self.fechapub.strftime('%Y/%m/%d'),
            'isbn': self.isbn
        }
        return jsonld_post
    
    @staticmethod
    def from_jsonld(json_book):
        name = json_book.get('name')
        author = json_book.get('author').get('name')
        datePublished = datetime.strptime(json_book.get('datePublished'), '%Y/%m/%d')
        isbn = json_book.get('isbn')
        if name is None or name == '':
            raise ValidationError('falta el nombre')
        elif author is None or author == '':
            raise ValidationError('falta el autor')
        elif datePublished is None or datePublished == '':
            raise ValidationError('falta la fecha')
        elif isbn is None or isbn == '':
            raise ValidationError('falta el isbn')
        return Book(nombre=name, autor=author,
                    fechapub=datePublished, isbn=isbn)
        
    
    
    
    
    
    
    
    