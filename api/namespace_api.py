from flask import request
from flask_restplus import Namespace, Resource
from flask_jwt_auth import APIAuth
from http_request_response import RequestUtilities
from http_request_args.validation import RequestArgsValidator


class NamespaceAPI:
    def __init__(self, api_name, business_obj, authorization_object, id_data_type='int',
                 post_qs_args_def=list(), post_body_args_def=list(),
                 get_qs_args_def=list(), get_body_args_def=list(),
                 update_body_args_def=list(), update_qs_args_def=list(),
                 delete_qs_args_def=list(), delete_body_args_def=list(),
                 get_all_qs_args_def=list(), get_all_body_args_def=list()):

        self.api_name = api_name
        self.api = Namespace(api_name, f'Operations related to the {api_name.lower()} namespace')
        self.business_obj = business_obj
        self.id_data_type = id_data_type
        self.authorization_object = authorization_object

        self.post_qs_args_def = post_qs_args_def
        self.post_body_args_def = post_body_args_def

        self.get_qs_args_def = get_qs_args_def
        self.get_body_args_def = get_body_args_def

        self.update_body_args_def = update_body_args_def
        self.update_qs_args_def = update_qs_args_def

        self.delete_qs_args_def = delete_qs_args_def
        self.delete_body_args_def = delete_body_args_def

        self.get_all_qs_args_def = get_all_qs_args_def
        self.get_all_body_args_def = get_all_body_args_def

    def create_crud_endpoints(self):
        @self.api.route('/')
        class ItemPost(Resource):
            ##### Post
            @RequestUtilities.try_except
            @APIAuth.auth_required(authorization_object=self.authorization_object['post'])
            @RequestArgsValidator.args_validation(self.post_qs_args_def, self.post_body_args_def)
            def post(inner_self):
                """ Create a new record  """
                return self.business_obj.create(request.body_args)

        @self.api.route('/<{}:id_>'.format(self.id_data_type))
        class Item(Resource):
            ##### Get

            @RequestUtilities.try_except
            @APIAuth.auth_required(authorization_object=self.authorization_object['get'])
            @RequestArgsValidator.args_validation(self.get_qs_args_def, self.get_body_args_def)
            def get(inner_self, id_):
                """ Get a record  """
                return self.business_obj.get(id_)

            ##### Update
            @RequestUtilities.try_except
            @APIAuth.auth_required(authorization_object=self.authorization_object['put'])
            @RequestArgsValidator.args_validation(self.update_qs_args_def, self.update_body_args_def)
            def put(inner_self, id_):
                """ update a record """
                return self.business_obj.update(id_, request.body_args)

            ##### Delete
            @RequestUtilities.try_except
            @APIAuth.auth_required(authorization_object=self.authorization_object['delete'])
            @RequestArgsValidator.args_validation(self.delete_qs_args_def, self.delete_body_args_def)
            def delete(inner_self, id_):
                """ Delete a record  """
                return self.business_obj.delete(id_)

        @self.api.route('/page')
        class ItemsCollection(Resource):

            @RequestUtilities.try_except
            @APIAuth.auth_required(authorization_object=self.authorization_object['page'])
            @RequestArgsValidator.args_validation(self.get_all_qs_args_def, self.get_all_body_args_def)
            def get(inner_self):
                """ Get a list of records  """
                return self.business_obj.get_all(request.qs_args)
