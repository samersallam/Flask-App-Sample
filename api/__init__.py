from flask_restplus import Api
from datetime import datetime
from resource.app_params import DataTimeParams

print('Creating the app APIs ...')


class NewApi(Api):
    def update_description(self, env_nam):
        self.description = 'Utility ({}) Deployed in {}'.format(env_nam,
                            datetime.now().strftime(DataTimeParams.date_time_format))


# Create the API
api = NewApi(
    Title='New Microservice',
    version='V1',
    description='Utility ({}) Deployed in {}',
    prefix='/v1'
)

from .dummy import api as dummy_api

# Add the namespaces to the API
api.add_namespace(dummy_api)
