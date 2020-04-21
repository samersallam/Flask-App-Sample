from flask import request
from flask_restplus import Namespace, Resource
from flask_jwt_auth import AuthFilters
from http_request_response import RequestUtilities
from http_request_args.validation import RequestArgsValidator


class NamespaceAPI:
    api_name = None
    api = None
    business_obj = None

    post_qs_args = None
    post_body_args = None

    get_qs_args = None
    get_body_args = None

    update_body_args = None
    update_qs_args = None

    delete_qs_args = None
    delete_body_args = None

    get_all_qs_args = None
    get_all_body_args = None

    @classmethod
    def set_up_namespace(cls, api_name, business_obj):
        cls.api_name = api_name
        cls.api = Namespace(api_name, f'Operations related to the {api_name.lower()} namespace')
        cls.business_obj = business_obj

    @classmethod
    def create_crud_endpoints(cls, post_qs_args_def=list(), post_body_args_def=list(),
                                   get_qs_args_def=list(), get_body_args_def=list(),
                                   update_body_args_def=list(), update_qs_args_def=list(),
                                   delete_qs_args_def=list(), delete_body_args_def=list(),
                                   get_all_qs_args_def=list(), get_all_body_args_def=list()):

        cls.post_qs_args_def = post_qs_args_def
        cls.post_body_args_def = post_body_args_def

        cls.get_qs_args_def = get_qs_args_def
        cls.get_body_args_def = get_body_args_def

        cls.update_body_args_def = update_body_args_def
        cls.update_qs_args_def = update_qs_args_def

        cls.delete_qs_args_def = delete_qs_args_def
        cls.delete_body_args_def = delete_body_args_def

        cls.get_all_qs_args_def = get_all_qs_args_def
        cls.get_all_body_args_def = get_all_body_args_def

        @cls.api.route('/')
        class ItemPost(Resource):
            ##### Post
            @RequestUtilities.try_except
            @AuthFilters.auth_required()
            @RequestArgsValidator.args_validation(cls.post_qs_args_def, cls.post_body_args_def)
            def post(self):
                """ Create a new record  """
                return cls.business_obj.create(request.body_args)

        @cls.api.route('/<int:id_>')
        class Item(Resource):
            ##### Get

            @RequestUtilities.try_except
            @AuthFilters.auth_required()
            @RequestArgsValidator.args_validation(cls.get_qs_args_def, cls.get_body_args_def)
            def get(self, id_):
                """ Get a record  """
                return cls.business_obj.get(id_)

            ##### Update
            @RequestUtilities.try_except
            @AuthFilters.auth_required()
            @RequestArgsValidator.args_validation(cls.update_qs_args_def, cls.update_body_args_def)
            def put(self, id_):
                """ update a record """
                return cls.business_obj.update(id_, request.body_args)

            ##### Delete
            @RequestUtilities.try_except
            @AuthFilters.auth_required()
            @RequestArgsValidator.args_validation(cls.delete_qs_args_def, cls.delete_body_args_def)
            def delete(self, id_):
                """ Delete a record  """
                return cls.business_obj.delete(id_)

        @cls.api.route('/page')
        class ItemsCollection(Resource):

            @RequestUtilities.try_except
            @AuthFilters.auth_required()
            @RequestArgsValidator.args_validation(cls.get_all_qs_args_def, cls.get_all_body_args_def)
            def get(self):
                """ Get a list of records  """
                return cls.business_obj.get_all(request.qs_args)
