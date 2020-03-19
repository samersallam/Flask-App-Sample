from flask import Flask
from config import EnvironmentConfig
from .logger import Logger
from flask_cors import CORS
from model import db, migrate
from service import Service
from service.db_admin import flk_admin, DBAdmin
from schema import ma
from jwt_auth import jwt
from api import api


def create_app(environment):
    # Get the configuration class
    config_class = EnvironmentConfig.get(environment)

    # Create the app
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Set up the logger
    Logger.set_up_app_loggers(app)

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app, send_wildcard=True)

    with app.app_context():
        # Initialize Plugins
        ##### DB Set up ####
        db.init_app(app)

        db_svc = Service(db)
        db_svc.set_db_charset(app.config['SQLALCHEMY_DATABASE_URI'])
        db_svc.db_create_all()

        if config_class.SQLALCHEMY_DB_RESET:
            db_svc.reset_sqlite_db()
            # db_svc.reset_mysql_db()

        flk_admin.init_app(app)
        if config_class.FLASK_ADMIN_ACTIVE:
            DBAdmin.create_admin_views(db)

        # Set up the database migration
        migrate.init_app(app, db)

        ##### End of  DB Set up ####

        ma.init_app(app)
        jwt.init_app(app)
        api.init_app(app)
        api.update_description(app.config['ENV_NAME'])
        # api.description = api.description.format(
        #     app.config['ENV_NAME'], datetime.now().strftime())

    return app
