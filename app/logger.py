"""
Useful URLs
https://www.youtube.com/watch?v=-ARI4Cz-awo
https://www.youtube.com/watch?v=jxmzY9soFXg

For aws
https://pypi.org/project/logbeam/
https://watchtower.readthedocs.io/en/latest/
"""


import logging
import watchtower
import boto3
import os

logging.basicConfig(level=logging.INFO)


class Logger:

    @staticmethod
    def create_watchtower_logger(environment, name, boto3_session, send_interval,
                                 log_group_retention_days, level):
        logger = logging.getLogger(name)

        if environment in ['Development', 'Testing']:
            handler = logging.StreamHandler()
        else:
            handler = watchtower.CloudWatchLogHandler(
                log_group='api_{}_logs'.format(environment),
                stream_name=name,
                boto3_session=boto3_session,
                send_interval=send_interval,
                log_group_retention_days=log_group_retention_days)

        handler.setLevel(level)
        logger.addHandler(handler)

        return logger

    @staticmethod
    def set_up_app_loggers(app):
        # Set up the app logger
        session = boto3.session.Session(region_name=os.environ['region_name'])
        environment = app.config['ENV_NAME']

        # Add the database loggers
        app.db_info_logger = Logger.create_watchtower_logger(
            environment=environment,
            name='database_info',
            boto3_session=session,
            send_interval=app.config['LOGGER_SEND_INTERVAL'],
            log_group_retention_days=app.config['LOG_GROUP_RETENTION_DAYS'],
            level=logging.INFO
        )

        app.db_exc_logger = Logger.create_watchtower_logger(
            environment=environment,
            name='database_exceptions',
            boto3_session=session,
            send_interval=app.config['LOGGER_SEND_INTERVAL'],
            log_group_retention_days=app.config['LOG_GROUP_RETENTION_DAYS'],
            level=logging.ERROR
        )

        # Add the app loggers
        app.app_info_logger = Logger.create_watchtower_logger(
            environment=environment,
            name='app_info',
            boto3_session=session,
            send_interval=app.config['LOGGER_SEND_INTERVAL'],
            log_group_retention_days=app.config['LOG_GROUP_RETENTION_DAYS'],
            level=logging.INFO
        )

        app.app_exc_logger = Logger.create_watchtower_logger(
            environment=environment,
            name='app_exceptions',
            boto3_session=session,
            send_interval=app.config['LOGGER_SEND_INTERVAL'],
            log_group_retention_days=app.config['LOG_GROUP_RETENTION_DAYS'],
            level=logging.ERROR
        )
        return app


# class RequestFormatter(logging.Formatter):
#     def format(self, record):
#         if has_request_context():
#             record.url = request.url
#             record.remote_addr = request.remote_addr
#         else:
#             record.url = None
#             record.remote_addr = None
#
#         return super().format(record)