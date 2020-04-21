from . import ma
from model import Dummy
from flask_marshmallow.fields import fields


class SeriesSchema(ma.ModelSchema):

    class Meta:
        model = Dummy


dummy_schema = SeriesSchema()
dummy_many_schema = SeriesSchema(many=True)
