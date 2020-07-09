import sqlite3

import pytest
from flaskr.db import get_db


# test if the connection is correctly closed after the context
def test_get_close_db(app):
    with app.get_context():
        db = get_db()
        assert db is get_db()

    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


# uses Pytest's monkeypatch fixture to replace init_db and called by runner
# init-db command should call the init_db function and return a message
def test_init_db_command(runner, monkeypatch):
    class Recorder(object):
        called = False

    def fake_init_db():
        Recorder.called = True

    monkeypatch.setattr('flaskr.db.init_db', fake_init_db)
    result = runner.invoke(args=['init-db'])
    assert 'initialized' in result.output
    assert Recorder.called
