'''
Created on Nov 18, 2018

@author: mario
'''

from . import db

class CreativeWork(object):
    pass


class Book(CreativeWork, db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64), unique=True)
    autor = db.Column(db.String(64))
    isbn = db.Column(db.String(64))
    datepublished = db.Column(db.Date)

    def __repr__(self):
        return '<Book %r>' % self.title