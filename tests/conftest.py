import pytest
from app import create_app, db
from config import TestConfig


@pytest.fixture(scope='function')
def app():
    app = create_app(config_object=TestConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    return app.test_client()


@pytest.fixture(scope='function')
def db_session(app):
    with app.app_context():
        yield db.session
