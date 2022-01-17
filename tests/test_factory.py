from flaskapp import create_app
import os
import pytest

def test_none_config():
    # Check create_app() fails when FLASK_ENV environment variable not set
    with pytest.raises(ValueError):
        try:
            del os.environ['FLASK_ENV']
        except:
            pass
        create_app()

def test_prod_config():
    os.environ['FLASK_ENV'] = 'prod'
    app = create_app()
    assert app.config['FLASK_ENV'] == 'prod'
    assert not app.config['DEBUG']
    assert not app.testing # probably stronger than "assert not app.create_app().config['TESTING']"

def test_dev_config():
    os.environ['FLASK_ENV'] = 'dev'
    app = create_app()
    assert app.config['FLASK_ENV'] == 'dev'
    assert app.config['DEBUG']
    assert not app.testing # probably stronger than "assert not app.create_app().config['TESTING']"

def test_testing_config():
    os.environ['FLASK_ENV'] = 'test'
    app = create_app()
    assert app.config['DEBUG'] 
    assert app.testing # probably stronger than "assert app.create_app().config['TESTING']"
    