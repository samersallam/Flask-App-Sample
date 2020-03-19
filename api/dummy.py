from flask_restplus import Namespace, Resource
# from jwt_auth.auth_filters import AuthFilters
# from .utility import RequestStatus, RequestModels

# Namespace
api = Namespace('dummy', 'Operations related to the dummy namespace')


@api.route('/dummy')
class DummyClass(Resource):
    # @RequestStatus.try_except
    # @AuthFilters.auth_required()
    def get(self):
        """ Get countries_names """
        return 'Hello World'
