from . import BusinessClass
from model import Dummy
from service import dummy_svc
from schema.dummy import dummy_schema, dummy_many_schema


class DummyBusiness(BusinessClass):
    pass


dummmy_business = DummyBusiness(Dummy, dummy_svc, dummy_schema, dummy_many_schema)
