import boto3
from flask import Flask
from flask_login import LoginManager
from flask_pymongo import PyMongo
from flask_wtf.csrf import CSRFProtect
from config import APP_CONFIG



CSRF = CSRFProtect()
MONGO = PyMongo()
LOGIN_MANAGER = LoginManager()
S3 = boto3.resource("s3")


def create_app(config_name):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(APP_CONFIG[config_name])

    CSRF.init_app(app)
    MONGO.init_app(app)
    LOGIN_MANAGER.init_app(app)
    LOGIN_MANAGER.login_view = 'auth.login'
    LOGIN_MANAGER.login_message = "You must be logged in to access this page."

    with app.app_context():
        from inception.core import cli
        from inception import home, admin, auth, jnatividad
        from inception.core.blueprints import bp_home, bp_admin, bp_auth, bp_api
        
        app.register_blueprint(bp_home, url_prefix='/')
        app.register_blueprint(bp_admin, url_prefix='/admin')
        app.register_blueprint(bp_auth, url_prefix='/auth')
        app.register_blueprint(bp_api, url_prefix='/api')
    return app
