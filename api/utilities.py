from flask import request, has_request_context
from flask import current_app as app
from flask_jwt_extended import get_jwt_identity
from functools import wraps
from resource.status_codes import var_bad_request


class RequestStatus:

    def __init__(self, status_code=None, data=None, message=None, function=None):
        self.status_code = status_code
        self.data = data
        self.message = self.__message_to_str(message)
        self.function = function

    def update(self, status_code=200, data=None, message=None, function=None):
        self.status_code = status_code
        self.data = data
        self.message = self.__message_to_str(message)
        self.function = function

    def __message_to_str(self, message):
        return message if message is None else str(message)

    def __call__(self, *args, **kwargs):
        return self.__dict__

    @staticmethod
    def get_request_context(exception=False):
        context = dict()
        if has_request_context():
            context['url'] = request.url
            context['remote_addr'] = request.remote_addr
            context['method'] = request.method

            if exception:
                # Add extra information in case of any exception
                context['headers'] = request.headers
                context['url_args'] = request.args
                context['body'] = request.json

            try:
                # Claims are not available in case of login endpoint and when the token is not provided
                claims = get_jwt_identity()
                if 'email' in claims:
                    context['email'] = claims['email']
            except:
                if request.json is not None and 'email' in request.json:
                    context['email'] = request.json['email']
                else:
                    context['email'] = 'Anonymous'

        return context

    @staticmethod
    def try_except(fn):
        """A decorator for all of the actions to do try except"""

        @wraps(fn)
        def wrapper(*args, **kwargs):
            try:
                # Action
                status, data = fn(*args, **kwargs)
                # Logging
                app.app_info_logger.info(RequestStatus.get_request_context())

            except Exception as e:
                status, data = var_bad_request, None
                status.update_msg(e)

                # Logging
                app.app_exc_logger.exception(RequestStatus.get_request_context(exception=True))

            rs = RequestStatus(status_code=status.code, message=status.message,
                               data=data, function=fn.__name__)
            return rs()

        return wrapper
