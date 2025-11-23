"""Flask application factory."""
import logging
from logging.handlers import RotatingFileHandler
import os

from flask import Flask
from config import get_config
from app.extensions import db, migrate, login_manager, init_extensions


def create_app(config=None, env=None):
    """Application factory function.
    
    Args:
        config: Optional config object or string name
        env: Optional environment string (development, testing, production)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    if config is None:
        config = get_config(env)
    elif isinstance(config, str):
        config = get_config(config)
    
    app.config.from_object(config)
    
    # Initialize extensions
    init_extensions(app)
    
    # Setup logging
    _setup_logging(app)
    
    # Register error handlers
    _register_error_handlers(app)
    
    # Register blueprints
    _register_blueprints(app)
    
    # Register CLI commands
    _register_cli_commands(app)
    
    # Register template filters and context processors
    _register_template_helpers(app)
    
    with app.app_context():
        # Create database tables
        db.create_all()
    
    return app


def _setup_logging(app):
    """Setup logging configuration."""
    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        file_handler = RotatingFileHandler(
            'logs/app.log',
            maxBytes=10240000,
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(app.config.get('LOG_LEVEL', 'INFO'))
        app.logger.addHandler(file_handler)
    
    app.logger.setLevel(app.config.get('LOG_LEVEL', 'INFO'))


def _register_error_handlers(app):
    """Register error handlers."""
    
    @app.errorhandler(404)
    def not_found(error):
        """Handle 404 errors."""
        return {'error': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Handle 500 errors."""
        db.session.rollback()
        app.logger.error(f'Server error: {error}')
        return {'error': 'Internal server error'}, 500
    
    @app.errorhandler(403)
    def forbidden(error):
        """Handle 403 errors."""
        return {'error': 'Forbidden'}, 403


def _register_blueprints(app):
    """Register all blueprints."""
    from app.blueprints.auth import auth_bp
    from app.blueprints.learning import learning_bp
    from app.blueprints.chat import chat_bp
    from app.blueprints.main import main_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(learning_bp)
    app.register_blueprint(chat_bp)


def _register_cli_commands(app):
    """Register CLI commands."""
    
    @app.shell_context_processor
    def make_shell_context():
        """Make database context available in shell."""
        return {'db': db}


def _register_template_helpers(app):
    """Register template filters and context processors."""
    
    @app.context_processor
    def inject_config():
        """Inject config into templates."""
        return {'config': app.config}
