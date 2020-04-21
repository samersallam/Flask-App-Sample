from sql_database_service.table_service import TableService
from model import db, Dummy


dummy_svc = TableService(db, Dummy)
