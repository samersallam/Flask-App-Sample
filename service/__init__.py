import time
from functools import wraps
from flask import current_app as app
from sqlalchemy import desc


class QueryStatus:
    def __init__(self, table, function, data=None, elapsed_time=None):
        self.table = table
        self.function = function
        self.data = data
        self.elapsed_time = elapsed_time

    def __repr__(self):
        return "Table: {}, Query: {}, Elapsed Time: {} [s]".format(
            self.table, self.function, self.elapsed_time)

    def query_log(self):
        return {
            'table': self.table,
            'query': self.function,
            'elapsed_time': self.elapsed_time
        }

    @staticmethod
    def return_query_status(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            st = time.clock()
            model_svc, data = fn(*args, **kwargs)
            et = time.clock() - st
            qs = QueryStatus(table=model_svc.table.__name__,
                             function=fn.__name__,
                             data=data,
                             elapsed_time=et)

            # Logging (Keep the import here)
            from api.utilities import RequestStatus
            app.db_info_logger.info(
                {**RequestStatus.get_request_context(), **qs.query_log()})

            return qs

        return wrapper


class Service:
    def __init__(self, database, table=None, per_page=10):
        self.database = database
        self.table = table
        self.per_page = per_page

    def query(self, row_filter=None, column_filter=list(), group_by=None, order_by=dict()):

        query = self.table.query

        # Rows filtering
        if row_filter is not None:
            query = query.filter(row_filter)

        # Columns filtering
        if len(column_filter) > 0:
            query = query.with_entities(*column_filter)

        # Grouping
        if group_by is not None:
            query = query.group_by(group_by)

        # Ordering
        if len(order_by) > 0:
            req_col = order_by['column'] if order_by['ascending'] else desc(order_by['column'])
            query = query.order_by(req_col)

        return query

    @QueryStatus.return_query_status
    def read(self, row_filter=None, column_filter=list(), group_by=None, order_by=dict(),
             count='first', page=None):
        """ Return query records """

        query = self.query(row_filter, column_filter, group_by, order_by)

        if count == 'first':
            return self, query.first()

        if page is None:
            return self, query.all()

        else:
            pager = query.paginate(per_page=self.per_page, page=page)
            return self, {'page': pager.items, 'num_pages': pager.pages}

    @QueryStatus.return_query_status
    def count(self, row_filter=None, column_filter=list()):
        """ Return number of records per query """
        query = self.query(row_filter, column_filter)
        return self, query.count()

    @QueryStatus.return_query_status
    def is_available(self, row_filter):
        """ Check if a record is available """

        qs = self.count(row_filter)
        return self, qs.data > 0

    @QueryStatus.return_query_status
    def create(self, new_record):
        """ Create a new record
            new_record: is an object of the model type
        """

        self.database.session.add(new_record)
        self.commit('create', self.table.__name__)
        return self, None

    @QueryStatus.return_query_status
    def update(self, id_, updated_record):
        """ Update an existing record
            updated_record: is a dictionary
        """

        query = self.query(self.table.id == id_)
        query.update(updated_record)
        self.commit('update', self.table.__name__)
        return self, None

    @QueryStatus.return_query_status
    def delete(self, id_):
        """ Delete an existing record """

        qs = self.read(self.table.id == id_)
        self.database.session.delete(qs.data)
        self.commit('delete', self.table.__name__)
        return self, None

    def commit(self, fn_name='Any', table_name='Any'):

        try:
            self.database.session.commit()

        except Exception as e:
            self.database.session.rollback()

            # Logging (Keep the import here)
            from api.utilities import RequestStatus
            app.db_exc_logger.exception({**RequestStatus.get_request_context(exception=True),
                                         **{'query': fn_name, 'table': table_name}})
            raise e

    # Some useful function to create the database
    def db_create_all(self):
        print('creating the new tables..')
        self.database.create_all()

    def db_drop_all(self):
        print('Dropping the old tables..')
        self.database.drop_all()

    def set_fk(self):
        # Activate foreign key checking
        self.database.engine.execute('SET FOREIGN_KEY_CHECKS = 1;')

    def reset_fk(self):
        # De-activate foreign key checking
        self.database.engine.execute('SET FOREIGN_KEY_CHECKS = 0;')

    def sqlite_enforce_fk_integrity(self):
        self.database.engine.execute('pragma foreign_keys = 1')

    def reset_mysql_db(self):
        self.reset_fk()
        self.db_drop_all()
        self.db_create_all()
        self.set_fk()

    def reset_sqlite_db(self):
        self.db_drop_all()
        self.db_create_all()
        self.sqlite_enforce_fk_integrity()

    def set_db_charset(self, db_uri):
        """
        This is required to make the database accept arabic characters
        To make sure that the database has been updated, use the following query
        SELECT default_character_set_name FROM information_schema.SCHEMATA
            WHERE schema_name = "db_name"; [USE THE QUOTES]
        :param db_uri: uri to connect with the database
        :return:
        """
        print('Set the db character set ...')

        if 'sqlite' in db_uri:
            # Do not use with sqlite
            return

        db_name = db_uri.split('/')[-1]
        self.database.engine.execute(
            'ALTER DATABASE {} CHARACTER SET UTF8MB4 COLLATE UTF8MB4_unicode_520_ci;'.format(db_name))

    def drop_alembic_version(self):
        self.database.engine.execute('DROP TABLE alembic_version;')

    def delete_table_content(self, table_name):
        self.database.engine.execute(
            # 'DELETE FROM {};'.format(self.table.__name__)
            'DELETE FROM {};'.format(table_name)
        )
