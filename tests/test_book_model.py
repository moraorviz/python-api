'''
Created on Nov 24, 2018

@author: mario
'''

import unittest
import time
from app import create_app, db
from app.models import Person, Book, CreativeWork
import datetime


class BookModelTestCase(unittest.TestCase):
    
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        
    def test_titulo_setter(self):
        b = Book(nombre='Crimen y Castigo')
        self.assertTrue(b.nombre is not None)
        
    def test_autor_setter(self):
        au = Person(nombre='Pedro', apellidos='Juan Gutiérrez')
        b = Book(autor = au)
        self.assertTrue(b.autor.nombre is not None)
        self.assertTrue(b.autor.apellidos is not None)
        
    def test_titulo_getter(self):
        b = Book(nombre='Crimen y Castigo')
        self.assertTrue(b.nombre == 'Crimen y Castigo')
        
    def test_autor_getter(self):
        au = Person(nombre='Pedro', apellidos='Juan Gutiérrez')
        b = Book(autor = au)
        self.assertTrue(b.autor.nombre=='Pedro')
        self.assertTrue(b.autor.apellidos=='Juan Gutiérrez')
        
    def test_valid_book_object(self):
        b = Book(nombre = 'Crimen y Castigo', 
                 autor = 'Fiodor Dostoyevski',
                 fechapub = datetime.date(1867, 1, 1))
        db.session.add(b)
        db.session.commit()
        self.assertTrue(b.id is not None)
        self.assertTrue(b.nombre == 'Crimen y Castigo')
        self.assertTrue(b.autor == 'Fiodor Dostoyevski')
        self.assertTrue(b.fechapub == datetime.date(1867, 1, 1))
        
    def test_valid_book_object2(self):
        au = Person(nombre='Fiodor', apellidos='Dostoyevski')
        fp = datetime.date(1867, 1, 1)
        cw = CreativeWork(nombre='Crimen y Castigo',
                          autor=au, fechapub = fp)
        b = Book(nombre=cw.nombre, autor=cw.autor.nombre + ' ' 
                 + cw.autor.apellidos,
                 fechapub=cw.fechapub)
        b.add_isbn('0-7582-3013-3')
        db.session.add(b)
        db.session.commit()
        self.assertTrue(b.fechapub == datetime.date(1867, 1, 1))
        self.assertTrue(b.id is not None)
        self.assertTrue(b.nombre == 'Crimen y Castigo')
        self.assertTrue(b.autor == 'Fiodor Dostoyevski')
        self.assertTrue(b.isbn == '0-7582-3013-3')
        
    def test_to_jsonld(self):
        print('Iniciando el test to json-ld')
        au = Person(nombre='Fiodor', apellidos='Dostoyevski')
        fp = datetime.date(1, 1, 1867)
        cw = CreativeWork(nombre='Crimen y Castigo',
                          autor=au, fechapub = fp)
        b = Book(nombre=cw.nombre, autor=cw.autor.nombre + ' ' 
                 + cw.autor.apellidos,
                fechapub=cw.fechapub)
        b.add_isbn('0-7582-3013-3')
        db.session.add(b)
        db.session.commit()
        with self.app.test_request_context('/'):
            json_book = b.to_jsonld()
        
        expected_keys = ['url', '@context', '@type', 'author', 'datePublished', 
                            'isbn', 'name']
        self.assertEqual(sorted(json_book.keys()), sorted(expected_keys))
        self.assertEqual('/python-api/v1/books/' + str(b.id), json_book['url'])
        
    def test_from_jsonld(self):
        print('Iniciando el test from json-ld')
        jsonld_request = {
            '@context': 'http://schema.org',
            '@type': 'Book',
            'name': 'Crimen y Castigo',
            'author': {
                '@type': 'Person',
                'name': 'Fiodor Dostoyevski'
            },
            'datePublished': '1867/01/01',
            'isbn': '0-7582-3013-3'
        }
        book = Book.from_json(jsonld_request)
        self.assertEqual(book.nombre, 'Crimen y Castigo')
        self.assertEqual(book.autor, 'Fiodor Dostoyevski')
        self.assertEqual(book.fechapub, '01/01/1867')
        self.assertEqual(book.isbn, '0-7582-3013-3')
        
        
    
    