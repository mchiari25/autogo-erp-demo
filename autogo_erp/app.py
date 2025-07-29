"""Entry point to run the AutoGo ERP Flask application.

This script imports the application factory from the package and runs
the development server when executed directly.  The host and port
parameters can be customized as needed.  The default host is
``127.0.0.1`` and the default port is ``5000``.

Usage::

    python app.py

Alternatively, you can run the app using the ``flask`` command line
interface after setting the ``FLASK_APP`` environment variable::

    export FLASK_APP=autogo_erp.app:create_app()
    flask run
"""

from autogo_erp import create_app


if __name__ == '__main__':
    # Create the Flask application using the default Config.
    app = create_app()
    # Run the development server with reloader and debugger enabled
    app.run(host='127.0.0.1', port=5000, debug=app.config.get('DEBUG', False))