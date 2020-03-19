from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
import jwt
from flask_jwt_extended.exceptions import WrongTokenError, NoAuthorizationError
from resource.status_codes import invalid_token, expired_token, missing_token, wrong_token


class AuthFilters:

    # A decorator for authentication and authorization purpose
    @staticmethod
    def auth_required():
        def decorator(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                try:

                    verify_jwt_in_request()

                    return fn(*args, **kwargs)

                except jwt.DecodeError:
                    # Token is not a valid JWT token
                    return invalid_token, None

                except NoAuthorizationError:
                    # The token is not provided
                    return missing_token, None

                except jwt.ExpiredSignatureError:
                    # The token is expired
                    return expired_token, None

                except WrongTokenError as e:
                    # To discriminate between refresh and access tokens
                    wrong_token.update_msg(str(e))
                    return wrong_token, None

            return wrapper

        return decorator
