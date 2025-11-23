"""Test Flask application factory."""
import pytest
from app import create_app
from config import DevelopmentConfig, TestingConfig, ProductionConfig, get_config


class TestAppFactory:
    """Test the app factory function."""
    
    def test_create_app_default(self):
        """Test creating app with default config (development)."""
        app = create_app()
        assert app is not None
        assert app.config['DEBUG'] is True
        assert 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']
    
    def test_create_app_development(self):
        """Test creating app with development config."""
        app = create_app(config=DevelopmentConfig)
        assert app is not None
        assert app.config['DEBUG'] is True
        assert app.config['TESTING'] is False
    
    def test_create_app_testing(self):
        """Test creating app with testing config."""
        app = create_app(config=TestingConfig)
        assert app is not None
        assert app.config['DEBUG'] is True
        assert app.config['TESTING'] is True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///:memory:'
    
    def test_create_app_production(self):
        """Test creating app with production config."""
        app = create_app(config=ProductionConfig)
        assert app is not None
        assert app.config['DEBUG'] is False
        assert app.config['TESTING'] is False
    
    def test_create_app_with_env_string(self):
        """Test creating app with environment string."""
        app = create_app(env='testing')
        assert app is not None
        assert app.config['TESTING'] is True
    
    def test_app_has_required_extensions(self):
        """Test that app has all required extensions initialized."""
        app = create_app(config=TestingConfig)
        
        with app.app_context():
            from app.extensions import db, migrate, login_manager
            assert db is not None
            assert migrate is not None
            assert login_manager is not None
    
    def test_app_has_blueprints(self):
        """Test that app has all required blueprints registered."""
        app = create_app(config=TestingConfig)
        
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        assert 'main' in blueprint_names
        assert 'auth' in blueprint_names
        assert 'learning' in blueprint_names
        assert 'chat' in blueprint_names
    
    def test_get_config_development(self):
        """Test getting development config."""
        config = get_config('development')
        assert config == DevelopmentConfig
    
    def test_get_config_testing(self):
        """Test getting testing config."""
        config = get_config('testing')
        assert config == TestingConfig
    
    def test_get_config_production(self):
        """Test getting production config."""
        config = get_config('production')
        assert config == ProductionConfig


class TestBlueprintRoutes:
    """Test that blueprints are properly registered with routes."""
    
    def test_main_blueprint_index_route(self, client):
        """Test main blueprint index route."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_auth_blueprint_login_route(self, client):
        """Test auth blueprint login route."""
        response = client.get('/auth/login')
        assert response.status_code == 200
    
    def test_auth_blueprint_register_route(self, client):
        """Test auth blueprint register route."""
        response = client.get('/auth/register')
        assert response.status_code == 200
    
    def test_learning_blueprint_route(self, client):
        """Test learning blueprint route."""
        response = client.get('/learning/')
        assert response.status_code == 200
    
    def test_chat_blueprint_requires_login(self, client):
        """Test that chat blueprint requires login."""
        response = client.get('/chat/')
        assert response.status_code == 302  # Redirect to login
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent')
        assert response.status_code == 404


class TestErrorHandlers:
    """Test error handling."""
    
    def test_app_has_error_handlers(self):
        """Test that app has error handlers registered."""
        app = create_app(config=TestingConfig)
        assert 404 in app.error_handler_spec[None]
        assert 500 in app.error_handler_spec[None]
        assert 403 in app.error_handler_spec[None]


class TestDatabaseInitialization:
    """Test database initialization."""
    
    def test_database_initialized_on_app_creation(self):
        """Test that database is initialized when app is created."""
        app = create_app(config=TestingConfig)
        
        with app.app_context():
            from app.extensions import db
            # If we get here without errors, db was properly initialized
            assert db.engine is not None
