from flask_jwt_extended import get_jwt_identity
from http_status_code.standard import successful_request, resource_not_found
from sql_database_service import RecordsPage
from sqlalchemy import func
from sqlalchemy.orm.exc import UnmappedInstanceError


class BusinessClassInterface:
    def create(self):
        pass

    def update(self):
        pass

    def process_args(self):
        pass

    def get(self):
        pass

    def get_all(self):
        pass

    def get_query_filter(self):
        pass

    def get_required_ordering(self):
        pass

    def delete(self):
        pass

    def delete_related_records(self):
        pass


class BusinessClass:

    def __init__(self, model, service, single_schema, many_schema, related_tables=list()):
        self.model = model
        self.service = service
        self.single_schema = single_schema
        self.many_schema = many_schema
        self.related_tables = related_tables  # List of tuples [(model, svc, field_id)]
        self.claims = dict()

    def create(self, model_args):
        self.process_args(model_args)
        new_record = self.model(model_args)
        self.service.create(new_record)

        return successful_request, self.single_schema.dump(new_record).data

    def update(self, id_, model_args):
        count = self.service.count(self.model.id == id_).data
        if count == 0:
            return resource_not_found, None

        self.process_args(model_args)
        print(model_args)
        self.service.update(id_, model_args)
        return successful_request, None

    def get_records(self, records_ids):
        return self.service.read(self.model.id.in_(records_ids), count='all').data

    def process_args(self, model_args):
        # To be implemented if the parameters are required to be processed
        # before creating or updating an object
        pass

    def get(self, id_):

        qs = self.service.read(self.model.id == id_)
        if qs.data:
            return successful_request, self.single_schema.dump(qs.data).data

        return resource_not_found, None

    def get_all(self, qs_args):
        page_number = qs_args.get('page_number')

        row_filter = self.get_query_filter(qs_args)
        order_by = self.get_required_ordering(qs_args)

        count = self.service.count(row_filter=row_filter).data

        if page_number:
            records = self.service.read(count='all', page=page_number,
                                        row_filter=row_filter, order_by=order_by).data['page']
            page = RecordsPage(count, self.many_schema.dump(records).data,
                               per_page=self.service.per_page, current_page=page_number)
        else:
            records = self.service.read(count='all', row_filter=row_filter, order_by=order_by).data
            page = RecordsPage(count, self.many_schema.dump(records).data)

        return successful_request, page.__dict__

    def get_query_filter(self, kwargs):
        # To be implemented if filtering is required
        return None

    def get_required_ordering(self, kwargs):
        # To be implemented if ordering is required
        return dict()

    def delete(self, id_):
        try:
            self.delete_related_records(id_)
            self.service.delete(id_)
            return successful_request, None

        except UnmappedInstanceError:
            return resource_not_found, None

    def delete_related_records(self, id_):

        for svc, field_name in self.related_tables:
            row_filter = getattr(svc.table, field_name) == id_
            records = svc.read(row_filter=row_filter, count='all').data

            for rec in records:
                svc.delete(rec.id)

    def set_related_tables(self, related_tables):
        # List of tuples [(svc, field_id)]
        self.related_tables = related_tables

    def is_duplicate_string(self, field_name, value, exclude_id=None, additional_filters=None):

        record = self.service.read(
            row_filter=(func.lower(getattr(self.model, field_name)) == value.lower()) & additional_filters).data

        if record is None or (record is not None and record.id == exclude_id):
            return False
        return True
