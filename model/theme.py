from . import db
from .db_params import DBParams


class Theme(db.Model):
    __tablename__ = 'theme'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(DBParams.tiny_str_len), unique=True, nullable=False)

    def __init__(self, payload):
        self.name = payload['name']
