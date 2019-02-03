import sqlite3

from flask import g
from os.path import join


DATABASE = join(__file__, '../poc.db')


def init_db(app):
    app.teardown_appcontext(close_db)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(exception=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
