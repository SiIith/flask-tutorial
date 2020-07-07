import sqlite3  # built-in sqlite support that handles writes sequentially

import click
from flask import current_app, g
from flask.cli import with_appcontext


# called when the application is handling requests and curr_app can be called
# g is an object unique for each request and stores information needed
def get_db():
    if 'db' not in g:
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


def init_db():
    # returns database connection
    db = get_db()

    # opens a file relative to the flaskr package. Executes script using the connection above
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# defines a command line command called init_db which calls the function
# returns success message
@click.command('init_db')
@with_appcontext
def init_db_command():
    # clears existing data and create new tables
    init_db()
    click.echo('Database is initialized')

# registers close_db and init_db_command so they can be used by the app
def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

