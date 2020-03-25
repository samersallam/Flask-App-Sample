from sql_database_service.table_service import TableService
from model import db, Theme

theme_svc = TableService(db, Theme)