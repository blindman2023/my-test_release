"""Pytest configuration and fixtures."""
import pytest
from app import create_app
from app.extensions import db
from config import TestingConfig


@pytest.fixture(scope='session')
def app():
    """Create and configure a test app instance."""
    app = create_app(TestingConfig)
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Provide a test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Provide a CLI test runner."""
    return app.test_cli_runner()


@pytest.fixture
def db_session(app):
    """Provide a database session."""
    with app.app_context():
        yield db
        db.session.rollback()
        db.session.remove()
