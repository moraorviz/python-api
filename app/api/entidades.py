'''
Created on Nov 25, 2018

@author: mario
'''

from flask import current_app, jsonify
from sqlalchemy import create_engine, inspect
from sqlalchemy.engine import reflection
from . import api


@api.route('/')
def get_entidades():
    print('Consultando entidades')
    engine = create_engine(current_app.config.get('SQLALCHEMY_DATABASE_URI'))
    inspector = inspect(engine)
    return jsonify({
        'entidades': [entidad for entidad in inspector.get_table_names()]
    })