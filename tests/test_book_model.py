'''
Created on Nov 24, 2018

@author: mario
'''

import unittest
import time
from app import create_app, db
from app.models import Book
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
        
    def test_titulo_getter(self):
        b = Book(nombre='Crimen y Castigo')
        self.assertTrue(b.nombre == 'Crimen y Castigo')
        
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
        
    
    