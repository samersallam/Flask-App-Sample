import datetime
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()


class Config(object):
    APPLICATION_NAME = 'Flask API Sample (SQL)'
    DEBUG = False
    TESTING = False

    # DB Config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False    # To print the sql query
    SQLALCHEMY_DB_RESET = False  # Do not change in any case

    # JWT Config
    JWT_SECRET_KEY = os.environ['SECRET_KEY']
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=5)
    JWT_HEADER_TYPE = ''
    JWT_HEADER_NAME = 'Authorization'

    # Flask Admin config
    FLASK_ADMIN_ACTIVE = False

    # Loggers parameters
    LOGGER_SEND_INTERVAL = 60   # [sec]
    LOG_GROUP_RETENTION_DAYS = 30  # [day]


if Config.SQLALCHEMY_DB_RESET:
    raise Exception('The SQLALCHEMY_DB_RESET should be false')


class DevelopmentConfig(Config):
    ENV_NAME = 'Development'
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ['DEVELOPMENT_DATABASE_URI']
    SQLALCHEMY_DB_RESET = True
    FLASK_ADMIN_ACTIVE = True


class TestingConfig(Config):
    ENV_NAME = 'Testing'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ['TEST_DATABASE_URI']


class StagingConfig(Config):
    ENV_NAME = 'Staging'
    SQLALCHEMY_DATABASE_URI = os.environ['STAGING_DATABASE_URI'] if 'STAGING_DATABASE_URI' in os.environ else None
    FLASK_ADMIN_ACTIVE = True


class ProductionConfig(Config):
    ENV_NAME = 'Production'
    SQLALCHEMY_DATABASE_URI = os.environ['PRODUCTION_DATABASE_URI'] if 'PRODUCTION_DATABASE_URI' in os.environ else None
    JWT_SECRET_KEY = os.environ['SECRET_KEY'] if 'SECRET_KEY' in os.environ else None


class EnvironmentConfig:

    configs = {
        'd': DevelopmentConfig,
        't': TestingConfig,
        's': StagingConfig,
        'p': ProductionConfig
    }

    @classmethod
    def get(cls, required_config):
        return cls.configs[required_config]
