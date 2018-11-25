'''
Created on Nov 24, 2018

@author: mario
'''

import unittest
import time
from app import create_app, db
from app.models import Person, CreativeWork
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
        
    def test_nombre_setter(self):
        au = Person(nombre='Pedro', apellidos='Juan Gutiérrez')
        fp = datetime.date(1867, 1, 1)
        cw = CreativeWork(nombre='El nido de la serpiente',
                          autor=au, fechapub = fp)
        self.assertTrue(cw.nombre is not None)
        self.assertTrue(cw.autor is not None)
        
    def test_fechapub_setter(self):
        au = Person(nombre='Pedro', apellidos='Juan Gutiérrez')
        fp = datetime.date(1867, 1, 1)
        cw = CreativeWork(nombre='El nido de la serpiente',
                          autor=au, fechapub=fp)
        self.assertTrue(cw.fechapub is not None)
        
        
    def test_nombre_getter(self):
        au = Person(nombre='Pedro', apellidos='Juan Gutiérrez')
        fp = datetime.date(1867, 1, 1)
        cw = CreativeWork(nombre='El nido de la serpiente',
                          autor=au, fechapub = fp)
        self.assertTrue(cw.nombre == 'El nido de la serpiente')
        self.assertTrue(cw.autor.nombre == 'Pedro')
        self.assertTrue(cw.autor.apellidos == 'Juan Gutiérrez')
        
    
    