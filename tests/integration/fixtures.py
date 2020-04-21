import pytest
from flask_jwt_extended import create_access_token
from sql_database_service.database_service import SQLiteDatabaseService
from app import create_app
from model import db


@pytest.fixture(scope='session', autouse=True)
def test_client():
    # 't' for the test environment
    app = create_app('t')

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = app.test_client()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    yield testing_client  # this is where the testing happens!

    ctx.pop()


@pytest.fixture(scope='function')
def log_in():
    def login_func(is_admin=True, user_id='aaaaa'):

        claims = {
            'id': user_id,
            'is_admin': is_admin,
            'email': 'dummy@email.com'
        }
        return create_access_token(identity=claims)
    return login_func


@pytest.fixture(scope='function', autouse=True)
def init_database(test_client):
    db_svc = SQLiteDatabaseService(db)
    db_svc.create_all()
    db_svc.enforce_sqlite_fk_integrity()
    yield None
    db_svc.drop_all()

@pytest.fixture(scope='function')
def create_db_record_fix():
    def create_new_record(model, svc, record):
        new_record = model(record)
        svc.create(new_record)
        return record
    return create_new_record


@pytest.fixture(scope='function')
def create_db_records_fix():
    def crete_new_records(model, svc, records):
        for record in records:
            new_record = model(record)
            svc.create(new_record)
        return records
    return crete_new_records


@pytest.fixture(scope='function')
def read_db_record_fix():
    def read_record(model, svc, schema, id_):
        available_rec = svc.read(model.id == id_)
        return schema.dump(available_rec.data).data
    return read_record