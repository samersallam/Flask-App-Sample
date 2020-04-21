

class DataInsertion:

    def __init__(self, data_generator):
        self.data_generator = data_generator

    def insert_all(self):
        pass

    @staticmethod
    def insert_records(records, model, svc, is_dict=True, process_record=None):
        for k, record in records.items():
            DataInsertion.insert_record(model, record, svc, is_dict, process_record)

    @staticmethod
    def insert_record(model, record, svc, is_dict=True, process_record=None):
        if process_record:
            record = process_record(record)

        if is_dict:
            new_record = model(record)
        else:
            new_record = model(**record)
        svc.create(new_record)


class DataBaseSeed:

    @staticmethod
    def seed():
        pass