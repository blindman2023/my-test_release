#!/usr/bin/env python
"""Flask CLI management script for database migrations, testing, and other tasks."""
import os
import sys
import click
from dotenv import load_dotenv
from flask.cli import FlaskGroup

# Load environment variables
load_dotenv()

from app import create_app
from app.extensions import db


def create_app_instance(info=None):
    """Create Flask app for CLI."""
    app = create_app()
    return app


@click.group(cls=FlaskGroup, create_app=create_app_instance)
def cli():
    """Flask CLI management."""
    pass


@cli.command()
def test():
    """Run unit tests."""
    import pytest
    sys.exit(pytest.main(['-v', 'tests/']))


@cli.command()
def seed():
    """Seed the database with sample data."""
    with create_app_instance().app_context():
        db.create_all()
        print('Database seeded!')


@cli.command()
@click.option('--message', '-m', prompt='Migration message', help='Migration message')
def create_migration(message):
    """Create a new database migration."""
    from flask_migrate import migrate
    migrate(message=message)
    print(f'Migration created: {message}')


if __name__ == '__main__':
    cli()
