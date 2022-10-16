import sqlite3
from flask import current_app, g
import click

def get_db() -> sqlite3.Connection:
    if 'db' in g: # request already contains a DB connection
        return g.db
    g.db = sqlite3.connect(
        current_app.config['DATABASE'],
        detect_types=sqlite3.PARSE_DECLTYPES
    )
    g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# DB init to execute as a command-line function
@click.command('init-db')
def init_db_command():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf-8'))
    click.echo('Initialized the database.')

def with_db(app):
    app.teardown_appcontext(close_db) # run after each request
    app.cli.add_command(init_db_command) # expose to 'flask' command
    return app
