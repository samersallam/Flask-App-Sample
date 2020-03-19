from flask_restplus import reqparse
from config import Config


class AuthModel:
    token_model = reqparse.RequestParser()
    token_model.add_argument(Config.JWT_HEADER_NAME, type=str,
                             required=True,
                             location='headers',
                             help='Murmurate access token')