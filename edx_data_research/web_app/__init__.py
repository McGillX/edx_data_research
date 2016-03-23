from flask import Flask, render_template

from edx_data_research.web_app.extensions import db, mail, security
from edx_data_research.web_app.parse import parse
from edx_data_research.web_app.public import public
from edx_data_research.web_app.report import report 


def create_app(config_object='config'):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_flask_security(app)
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    """Register extensions"""
    db.init_app(app)
    mail.init_app(app)


def register_flask_security(app):
    """Register Flask-Security extension"""
    from flask.ext.security import MongoEngineUserDatastore

    from edx_data_research.web_app.auth.forms import ExtendedRegisterForm
    from edx_data_research.web_app.models import User, Role

    user_datastore = MongoEngineUserDatastore(db, User, Role)
    security.init_app(app, user_datastore, register_form=ExtendedRegisterForm)


def register_blueprints(app):
    """Register blueprints"""
    app.register_blueprint(parse)
    app.register_blueprint(public)
    app.register_blueprint(report)


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        error_code = getattr(error, 'code', 500)
        return render_template('errors/{0}.html'.format(error_code)), error_code
    for error_code in [404, 500]:
        app.errorhandler(error_code)(render_error)
