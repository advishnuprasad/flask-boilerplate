import logging
import traceback

from flask import Flask, jsonify
from flask_cors import CORS
from marshmallow import ValidationError

from myapp import manage
from myapp.auth.api import auth_api
from myapp.auth.oauth2 import config_oauth
from myapp.commons.exceptions import ForbiddenException, UnauthorizedException
from myapp.extensions import authorize, celery, db, jwt, migrate
from myapp.users.api import users_api

logger = logging.getLogger("myapp.app")


def create_app(testing=False):
    """Application factory, used to create application"""
    app = Flask("app", template_folder="templates")
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object("myapp.config")

    if testing is True:
        app.config["TESTING"] = True

    configure_extensions(app)
    configure_cli(app)
    register_blueprints(app)
    config_oauth(app)
    init_celery(app)

    @app.errorhandler(Exception)
    def handle_known_exceptions(exception):
        logger.error(traceback.format_exc())

        if isinstance(exception, ValidationError):
            return jsonify(code=400, message=exception.messages), 400

        elif isinstance(exception, ForbiddenException):
            return jsonify(code=403, message=exception.messages), 403

        elif isinstance(exception, (UnauthorizedException)):
            return jsonify(code=401, message=exception.messages), 401

        # FIXME It should be disabled after sometime. Exposing the exceptions to frontend is not a good practice
        return (
            jsonify(
                code=500,
                message={
                    "_entity": [
                        f"Something went wrong! Please try again later! {exception}"
                    ]
                },
            ),
            403,
        )

    return app


def configure_extensions(app):
    """Configure flask extensions"""
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    authorize.init_app(app)


def configure_cli(app):
    """Configure Flask 2.0's cli for easy entity management"""
    app.cli.add_command(manage.init)


def register_blueprints(app):
    """Register all blueprints for application"""
    app.register_blueprint(users_api, url_prefix="/api/v1")
    app.register_blueprint(auth_api)


def init_celery(app=None):
    app = app or create_app()
    celery.conf.update(app.config.get("CELERY", {}))

    class ContextTask(celery.Task):
        """Make celery tasks work with Flask app context"""

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
