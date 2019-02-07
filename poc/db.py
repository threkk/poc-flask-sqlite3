import sqlite3
import click

from flask import g, current_app
from flask.cli import with_appcontext
from os import environ
from os.path import dirname, exists, join


DEFAULT_DB = '../poc.db'
SCHEMA_PATH = '../schema.sql'


def init_db(app):
    """
    Registers the database object in the context and the command in the cli
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(populate_db)


@click.command('db:populate')
@with_appcontext
def populate_db():
    """CLI command to populate empty databases. Database must exist."""
    db = get_db()
    with current_app.open_resource(SCHEMA_PATH, 'r') as f:
        db.executescript(f.read())
    db.commit()
    click.echo('Database created.')


def get_db():
    """Opens a connection to the database and stores it in the global object"""
    if 'db' not in g:
        # Get the database from the environment.
        db_path = join(dirname(__file__),
                       environ.get('DB', default=DEFAULT_DB))

        if not exists(db_path):
            raise FileNotFoundError(f'{db_path} does not exists')

        # Initialise a connection and add it to the global object.
        g.db = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)

        # Tells the connection to return rows that behave like dicts.
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(exception=None):
    """Closes the database connection when leaving the context"""
    # Remove the reference from the global object.
    db = g.pop('db', None)

    if db is not None:
        # Close the connection.
        db.close()
