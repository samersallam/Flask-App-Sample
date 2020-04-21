from flask_restplus import Api
from datetime import datetime
from resource.app_params import DataTimeParams
from config import Config

print('Creating the app APIs ...')


class NewApi(Api):
    def update_description(self, env_nam):
        self.description = '{} ({}) Deployed in {}'.format(Config.APPLICATION_NAME, env_nam,
                            datetime.now().strftime(DataTimeParams.date_time_format))


# Create the API
api = NewApi(
    Title=Config.APPLICATION_NAME,
    version='V1',
    description='Utility ({}) Deployed in {}',
    prefix='/v1'
)


from .dummy_namespace import DummyAPI


# Add the namespaces to the API
api.add_namespace(DummyAPI.api)

