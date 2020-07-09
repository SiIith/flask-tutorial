import os
import tempfile

import pytest
from flaskr import create_app
from flaskr.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    # create a temporary file, returns file object and path
    db_fd, db_path = tempfile.mkdtemp()

    # switch TESTING to true and overrides database path to the temp file
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


# fixture that calls test_client and test on it without opening the server
@pytest.fixture
def client(app):
    return app.test_client()


# calls the Click commands registered w/ the application
@pytest.fixture
def runner(app):
    return app.test_cli_runner()

