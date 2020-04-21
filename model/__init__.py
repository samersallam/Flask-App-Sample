from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from resource.db_params import DBParams

print('Creating the DB ..')
db = SQLAlchemy()
migrate = Migrate()

from .dummy import Dummy
