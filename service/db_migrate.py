"""
For migration setup for the first time in the cmd:
python -m service.db_migrate -env d  db init

For detection the new changes:
python -m service.db_migrate -env d  db migrate

To upgrade to the new schema:
python -m service.db_migrate -env d  db upgrade

To downgrade to the old schema:
python -m service.db_migrate -env d  db downgrade


If you want to be able to see all of the database schema migrations:
python -m service.db_migrate db history

If you want to see the current version of the database schema:
python -m service.db_migrate db current --verbose

If you want to see a list of commands that you can use with Flask-Migrate:
python -m service.db_migrate db --help

A useful URL:
https://www.youtube.com/watch?v=BAOfjPuVby0&t=384s

A useful URL for migration with non-nullable columns
https://medium.com/the-andela-way/alembic-how-to-add-a-non-nullable-field-to-a-populated-table-998554003134

Useful bug:
https://stackoverflow.com/questions/32311366/alembic-util-command-error-cant-find-identifier

Detect minor changes:
https://stackoverflow.com/questions/58532518/why-flask-migrations-does-not-detect-a-fields-length-change
"""

from app import create_app

from flask_migrate import Manager, MigrateCommand

# Set up the database migration
manager = Manager(create_app)

manager.add_command('db', MigrateCommand)
manager.add_option("-env", "--environment", default='d', required=False)

if __name__ == '__main__':
    manager.run()

