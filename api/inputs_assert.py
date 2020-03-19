import re
from flask import request


class ParamsAssert:

    def __init__(self, payload=dict()):
        self.payload = payload
        self.missing_fields = list()
        self.payload_problem = False
        self.report = ''

    def payload_has_problem(self):
        self.payload_problem = True

    def check_missing_fields(self):
        if len(self.missing_fields):
            self.update_report('The following fields {} are missing'.format(self.missing_fields))

    def update_report(self, report_update):
        self.report += report_update + '\n'
        self.payload_has_problem()

    def check_str_length(self, key, length=None):
        if len(self.payload[key]) < 1 or self.payload[key].isspace():
            self.update_report('The {} cannot be empty or white spaces'.format(key))
            return False

        if length and len(self.payload[key]) > length:
            self.update_report('The {} length cannot be longer than {}'.format(key, length))
            return False
        return True

    def check_str_match_pattern(self, key, pattern):
        if not re.search(pattern, self.payload[key]):
            self.update_report('Invalid {} pattern'.format(key))
            return False
        return True

    def check_capitalized_string(self, key):
        """ This function check if the first letter of each word is Capital """
        words = self.payload[key].split(' ')
        for word in words:
            if word[0].islower():
                self.update_report('The first letter of each word in {} must be Capital. Ex: United States'.format(key))
                return False
        return True

    def in_payload(self, key):
        raise NotImplementedError

    def has_data_type(self, key, data_type):
        raise NotImplementedError

    # All method sharing the same functionality over request body and request qs


class QueryStringAssert(ParamsAssert):

    def __init__(self, payload):
        super().__init__(payload)

    def has_data_type(self, key, data_type):
        try:
            data_type(self.payload[key])
        except:
            self.update_report('The {} should be of type {}'.format(key, data_type.__name__))
            return False
        return True

    def in_payload(self, key):
        # Request parser .parse() returns all model args
        # For non provided args the default value is None
        if self.payload[key] is None:
            return False

        return True

    @staticmethod
    def assert_request_parser(models):
        """
        :param models: (list)
        :return: parsing_problem: bool
                 content: - error message if parsing_problem True
                          - args dict if parsing_problem False
        """
        args_dict = dict()
        models_keys = dict()
        missing_fields = list()
        parsing_problem = False

        for model in models:
            try:
                model_args = model.parse_args()
                args_dict.update(model_args)
            except:
                parsing_problem = True
                req_args = request.args.to_dict()
                for arg in model.args:
                    arg_type = arg.type.__name__
                    models_keys[arg.name] = {'type': arg_type if arg.action != 'append'
                                             else 'list of {}'.format(arg_type)}
                    if arg.required and arg.name not in req_args.keys():
                        missing_fields.append(arg.name)

        if parsing_problem and len(missing_fields):
            return parsing_problem, 'Missing required fields {} in the query string'.format(missing_fields)
        elif parsing_problem:
            return parsing_problem, 'Expected args {}'.format(models_keys)
        else:
            return parsing_problem, args_dict


class BodyAssert(ParamsAssert):
    def __init__(self, payload):
        super().__init__(payload)

    def has_data_type(self, key, data_type):
        if type(self.payload[key]) is not data_type:
            self.update_report('The {} should be of type {}'.format(key, data_type.__name__))
            return False
        return True

    def in_payload(self, key):
        if key not in self.payload.keys():
            self.update_report('The following field {} is missing in request body'.format(key))
            return False
        return True


class RequestAssert:
    def __init__(self, query_string=dict(), body=dict()):
        self.qs = QueryStringAssert(query_string)
        self.body = BodyAssert(body)
        self.request_problem = False
        self.final_report = ''

    def check_overall_request(self):
        if self.qs.payload_problem:
            self.request_problem = True
            # self.final_report += 'You have the following problems in the URL query string:\n'
            self.final_report += self.qs.report

        if self.body.payload_problem:
            self.request_problem = True
            # self.final_report += 'You have the following problems in the request body:\n'
            self.final_report += self.body.report

        return self.request_problem

    # Videos map and videos analysis
    def check_string_input(self, key, capitalized=False, input_options=list(), str_len=None):
        if not self.qs.in_payload(key):
            return

        if not self.qs.has_data_type(key, str):
            return

        if not self.qs.check_str_length(key, str_len):
            return

        # Check Capitals
        if capitalized:
            if not self.qs.check_capitalized_string(key):
                return

        # Check word options
        if len(input_options):
            if self.qs.payload[key] not in input_options:
                self.qs.update_report('{} should be one of, {}'.format(key, input_options))
                return

    # Videos map and videos analysis
    def check_top_n(self):
        if not self.qs.in_payload('top_n'):
            return

        if not self.qs.has_data_type('top_n', int):
            return

        if self.qs.payload['top_n'] < 1:
            self.qs.update_report('top_n can not be less than 1')
