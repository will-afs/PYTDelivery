""""This file contains setup functions called fixtures that each test will use"""

import os
import tempfile

import pytest
# import unittest

from flaskapp import create_app
from flaskapp.db.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    # tempfile.mkstemp() creates and opens a temporary file, returning the file descriptor 
    # and the path to it. The DATABASE path is overridden so it points to this temporary 
    # path instead of the instance folder. After setting the path, the database tables are 
    # created and the test data is inserted. After the test is over, the temporary file is 
    # closed and removed.
    db_fd, db_path = tempfile.mkstemp()

    # TESTING tells Flask that the app is in test mode. Flask changes some internal behavior 
    # so it’s easier to test, and other extensions can also use the flag to make testing
    #  them easier.
    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })


    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    # The client fixture calls app.test_client() with the application object created by the app 
    # fixture. Tests will use the client to make requests to the application without running the
    #  server.
    return app.test_client()


@pytest.fixture
def runner(app):
    # The runner fixture is similar to client. app.test_cli_runner() creates a runner that can 
    # call the Click commands registered with the application.The runner fixture is similar to 
    # client. app.test_cli_runner() creates a runner that can call the Click commands registered 
    # with the application.
    return app.test_cli_runner()