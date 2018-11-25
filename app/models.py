'''
Created on Nov 24, 2018

@author: mario
'''

from . import db

class Thing:
    def __init__(self, nombre):
        self.nombre = nombre


class CreativeWork(Thing):
    def __init__(self, nombre, autor):
        super().__init__(nombre)
        self.autor = autor
    
    
class Book(db.Model, CreativeWork):
    __tablename__ = 'libros'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True)
    autor = db.Column(db.String(64))
    fechapub = db.Column(db.Date)
    def __init__(self, **kwargs):
        super(Book, self).__init__(**kwargs)
        
    def __repr__(self):
        return '<User %r>' % self.nombre