from model import Dummy
from schema.dummy import dummy_schema, dummy_many_schema
from service import dummy_svc
from . import BusinessClass


class DummyBusiness(BusinessClass):
    pass


dummmy_business = DummyBusiness(Dummy, dummy_svc, dummy_schema, dummy_many_schema)
