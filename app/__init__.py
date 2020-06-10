from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from sql_database_service.database_service import SQLiteDatabaseService, MySQLDatabaseService

from api import api
from business.seed import DataBaseSeed
from config import EnvironmentConfig
from model import db, migrate
from schema import ma
from service.db_admin import flk_admin, DBAdmin
from .logger import Logger


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

        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if 'sqlite' in db_uri:
            db_svc = SQLiteDatabaseService(db)
        elif 'mysql' in db_uri:
            db_svc = MySQLDatabaseService(db)
            db_svc.set_charset(app.config['SQLALCHEMY_DATABASE_URI'])

        if config_class.SQLALCHEMY_DB_RESET:
            db_svc.reset()
            DataBaseSeed.seed()
        else:
            db_svc.create_all()

        flk_admin.init_app(app)
        if config_class.FLASK_ADMIN_ACTIVE:
            DBAdmin.create_admin_views(db)

        # Set up the database migration
        migrate.init_app(app, db)

        ##### End of  DB Set up ####

        # Set up jwt manager
        jwt = JWTManager()
        jwt.init_app(app)

        # Setup the app schemas
        ma.init_app(app)

        # Set up the app namespaces
        api.init_app(app)
        api.update_description(app.config['ENV_NAME'])

    return app
