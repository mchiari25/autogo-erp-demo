"""Initialization for the AutoGo ERP package.

This module configures the Flask application and SQLAlchemy database.  It
exposes a factory function ``create_app`` used by the ``flask`` command
line interface to create and run the web application.  Separating the
application creation into a factory makes testing and configuration
easier because the same code can be reused with different settings.

Usage::

    from autogo_erp import create_app
    app = create_app()
    app.run()

The configuration is loaded from ``config.py`` and may be overridden by
setting the ``AUTOERP_SETTINGS`` environment variable to point at a
custom Python file.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

# Initialize the SQLAlchemy instance.  The actual database engine will be
# bound to a Flask app inside ``create_app``.
db = SQLAlchemy()


def create_app(config_class: type[Config] | None = None) -> Flask:
    """Application factory to create and configure the Flask app.

    Args:
        config_class: Optional configuration class.  If omitted, uses
            ``Config`` from ``autogo_erp.config``.

    Returns:
        A configured :class:`~flask.Flask` application instance.
    """
    app = Flask(__name__)
    # Load default configuration
    app.config.from_object(config_class or Config)

    # Initialize database
    db.init_app(app)

    # Register blueprints/routes
    from .views import bp as main_bp
    app.register_blueprint(main_bp)

    # Create the database tables if they don't exist yet.  In a real
    # project you might use a migration tool like Alembic to handle
    # schema changes, but for this simple example we'll create tables
    # automatically at startup.
    with app.app_context():
        db.create_all()

    return app