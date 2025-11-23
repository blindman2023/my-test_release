"""Flask extensions initialization."""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from marshmallow import Schema


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def init_extensions(app):
    """Initialize all Flask extensions with the app."""
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    # Set login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    return db, migrate, login_manager
