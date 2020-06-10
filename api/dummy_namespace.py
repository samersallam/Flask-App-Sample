from http_request_args.argument import StringArgument, NumberArgument

from business.dummy import dummmy_business
from .namespace_api import NamespaceAPI


class DummyAPI(NamespaceAPI):
    pass


authorization_object = {'post': None, 'get': None, 'put': None, 'delete': None, 'page': None}

dummy_api = DummyAPI('dummy', dummmy_business, authorization_object,
                     post_body_args_def=[StringArgument('name', required=True)],
                     update_body_args_def=[StringArgument('name', required=True)],
                     get_all_qs_args_def=[NumberArgument('page_number', arg_type=int, required=False)]
                     )

dummy_api.create_crud_endpoints()
