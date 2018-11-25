'''
Created on Nov 25, 2018

@author: mario
'''

from flask import current_app
from sqlalchemy import create_engine
from sqlalchemy.engine import reflection
from . import api


@api.route('/')
def get_entidades():
    print('Consultando entidades')
    engine = create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URI'))
    insp = reflection.Inspector.from_engine(engine)
    entities = insp.get_table_names()
    return entities