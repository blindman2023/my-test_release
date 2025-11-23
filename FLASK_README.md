# Flask Application Structure

This is a production-ready Flask application with a modular blueprint architecture.

## Project Structure

```
.
├── app/                          # Main Flask application package
│   ├── __init__.py              # App factory (create_app)
│   ├── extensions.py            # Flask extensions initialization
│   ├── blueprints/              # Application blueprints
│   │   ├── __init__.py
│   │   ├── main.py             # Main routes (homepage, about)
│   │   ├── auth.py             # Authentication routes
│   │   ├── learning.py         # Learning/course routes (学习)
│   │   └── chat.py             # Chat functionality (聊天)
│   └── templates/              # Jinja2 templates
│       ├── base.html           # Base template with Bootstrap layout
│       ├── index.html          # Homepage
│       ├── about.html          # About page
│       ├── auth/               # Authentication templates
│       │   ├── login.html      # Login page with navbar placeholder
│       │   └── register.html   # Registration page
│       ├── learning/           # Learning templates
│       │   ├── index.html
│       │   ├── courses.html
│       │   ├── course_detail.html
│       │   └── progress.html
│       └── chat/               # Chat templates
│           └── index.html
├── config.py                    # Configuration settings (Development, Testing, Production)
├── wsgi.py                      # WSGI entry point for production servers
├── manage.py                    # CLI management script
├── pytest.ini                   # Pytest configuration
├── requirements-flask.txt       # Flask dependencies
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore rules
└── tests/                       # Test suite
    ├── __init__.py
    ├── conftest.py             # Pytest fixtures and configuration
    └── test_app_factory.py     # App factory tests
```

## Features

- **App Factory Pattern**: `create_app()` function in `app/__init__.py` for flexible configuration
- **Modular Blueprints**: Separate blueprints for auth, learning, and chat functionality
- **Extensions**: Centralized Flask extensions in `app/extensions.py`:
  - Flask-SQLAlchemy for ORM
  - Flask-Migrate for database migrations
  - Flask-Login for user authentication
  - Marshmallow for serialization (ready to use)
- **Configuration Management**: Environment-based configs in `config.py`
  - Development: Debug mode, SQLite
  - Testing: In-memory database, CSRF disabled
  - Production: Hardened security settings
- **Jinja2 Templates**: Bootstrap 5 responsive UI with Chinese language support
  - Navbar with placeholders for 学习 (Learning), 聊天 (Chat), 登录 (Login)
  - Flash message handling
  - Responsive layout
- **Error Handling**: Custom error handlers for 404, 403, and 500 errors
- **Logging**: Configured logging with rotating file handlers in production
- **Testing**: Pytest fixtures and comprehensive app factory tests
- **CLI Management**: `manage.py` for database migrations and tests

## Getting Started

### Installation

1. Install dependencies:
```bash
pip install -r requirements-flask.txt
```

2. Setup environment variables:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Create database and tables:
```bash
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

### Running the Application

Development mode:
```bash
export FLASK_APP=wsgi.py
export FLASK_ENV=development
flask run
```

Or using the WSGI entry point for production:
```bash
gunicorn wsgi:app
```

### Running Tests

```bash
pytest
# or
python manage.py test
```

## Environment Configuration

Create a `.env` file based on `.env.example`:

```env
FLASK_APP=wsgi.py
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///app.db
LOG_LEVEL=DEBUG
```

Environment variables:
- `FLASK_ENV`: Environment (development, testing, production)
- `SECRET_KEY`: Session encryption key
- `DATABASE_URL`: SQLAlchemy database URI
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR)

## Adding Models

Create model files in `app/models/` and import them in `app/__init__.py`:

```python
from app.models import User, Course, Message
```

## Adding Routes

Create new blueprints in `app/blueprints/` and register them in `app/__init__.py`:

```python
from app.blueprints.my_blueprint import my_bp
app.register_blueprint(my_bp)
```

## Database Migrations

Using Flask-Migrate (Alembic):

```bash
# Create initial migration
python manage.py db init

# Create migration after model changes
python manage.py db migrate -m "Add new column"

# Apply migration
python manage.py db upgrade

# Rollback migration
python manage.py db downgrade
```

## Deployment

For production deployment:
1. Set `FLASK_ENV=production`
2. Use a production WSGI server (gunicorn, uWSGI)
3. Configure proper database (PostgreSQL recommended)
4. Set `SECRET_KEY` to a secure value
5. Enable HTTPS/SSL
6. Configure logging and monitoring

Example with gunicorn:
```bash
gunicorn -w 4 -b 0.0.0.0:8000 wsgi:app
```

## Development Tips

- Use `flask shell` for interactive debugging
- Set `SQLALCHEMY_ECHO=True` in development to see SQL queries
- Use `flask routes` to list all registered routes
- Check `logs/app.log` for application logs

## Project Highlights for Testing

The `tests/test_app_factory.py` file contains comprehensive tests that verify:
- App creation with different configurations (development, testing, production)
- Environment-based config selection
- All extensions are properly initialized
- All blueprints are registered
- All routes are accessible
- Error handlers are properly registered
- Database initialization works correctly

Run tests with:
```bash
pytest tests/test_app_factory.py -v
```
