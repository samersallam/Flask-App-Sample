from . import db
from . import DBParams


class Dummy(db.Model):
    __tablename__ = 'dummy'
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    name = db.Column(db.String(DBParams.tiny_str_len), nullable=False)

    # dummydeps
    # dummydeps = db.relationship('DummyDep', backref=db.backref('dummy'))

    def __init__(self, payload):
        self.name = payload['name']