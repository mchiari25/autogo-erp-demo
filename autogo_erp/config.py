"""Configuration for the AutoGo ERP application.

This file defines a simple configuration class used by Flask.  For a
lightweight ERP prototype we store data in a local SQLite database.
Additional settings such as secret keys and debug flags are specified
here as well.
"""

import os
from pathlib import Path


class Config:
    """Base configuration class.

    Attributes:
        SECRET_KEY: Flask uses this key to secure session data.  In a
            production setting you should generate a random key and
            keep it secret.  For development purposes this default
            value suffices.
        SQLALCHEMY_DATABASE_URI: URI to the SQLite database file.  The
            path is resolved relative to this file's directory so that
            running the application from different working directories
            still locates the same database.  If you wish to store the
            database elsewhere, set the ``AUTOERP_DB_PATH`` environment
            variable to an absolute path.
        SQLALCHEMY_TRACK_MODIFICATIONS: Disables a feature that tracks
            modifications of objects and signals events.  Turning it
            off saves memory and is recommended unless you need those
            signals.
    """

    # Basic secret key for session management.  Override this in
    # production via environment variable.
    SECRET_KEY = os.environ.get("AUTOERP_SECRET_KEY", "dev-secret-key")

    # Determine the database location.  Use an environment variable if
    # provided; otherwise place the database in the package directory.
    _default_db_path = Path(os.environ.get("AUTOERP_DB_PATH", Path(__file__).resolve().parent / "autogo.db"))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{_default_db_path}"

    # Disable SQLAlchemy event system overhead
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Enable Flask debug mode when running locally.  This should be
    # disabled in production.
    DEBUG = os.environ.get("AUTOERP_DEBUG", "1") == "1"
    # Paths for AutoGo branding
    LOGO_PATH = "static/images/logo_autogo.png"
    LOGO_SMALL_PATH = "static/images/logo_autogo_small.png"
    FAVICON_PATH = "static/images/favicon_autogo.png"

