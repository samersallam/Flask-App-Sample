from flask_restplus import Namespace, Resource
from .http_request_args.argument import StringArgument, NumberArgument, ListArgument
from .http_request_args.validation import RequestArgsValidator
from business.theme import ThemeBusiness

# from jwt_auth.auth_filters import AuthFilters
# from .utility import RequestStatus, RequestModels

# Namespace
api = Namespace('dummy', 'Operations related to the dummy namespace')

# For the query string
qs_args_def = [
    StringArgument(name='country_name', required= True, req_options=['Syria']),
    NumberArgument(name='country_id', required=True, arg_type=int),
    ListArgument(name='cities', required=True, arg_obj=StringArgument(name='', required=True))
]

# For the body
body_args_def = [
    NumberArgument(name='a_num', required=True, arg_type=int, req_range=[1,3], req_options=[2,4,5]),
    StringArgument(name='b_str', required=True, regex_pattern='^g')
]



@api.route('/dummy')
class DummyClass(Resource):
    # @RequestStatus.try_except
    # @AuthFilters.auth_required()
    def get(self):
        """ Get  """
        req_validator = RequestArgsValidator(qs_args_def, body_args_def, api.payload)
        req_validator.validate()

        if req_validator.invalid:
            return req_validator.report
        else:
            return req_validator.body_args


@api.route('/db_test')
class DummyClass(Resource):
    # @RequestStatus.try_except
    # @AuthFilters.auth_required()
    def get(self):
        """ Get  """
        return ThemeBusiness.test_theme_table()