from http_request_args.argument import StringArgument, NumberArgument
from business.dummy import dummmy_business
from .namespace_api import NamespaceAPI


class DummyAPI(NamespaceAPI):
    pass


DummyAPI.set_up_namespace('dummy', dummmy_business)
DummyAPI.create_crud_endpoints(
    # Post
    post_body_args_def=[StringArgument('name', required=True)],
    # Update
    update_body_args_def=[StringArgument('name', required=True)],
    # Get All
    get_all_qs_args_def=[NumberArgument('page_number', arg_type=int, required=False)]
)
