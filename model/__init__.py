from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

print('Creating the DB ..')
db = SQLAlchemy()
migrate = Migrate()
