"""
A useful URL
https://www.youtube.com/watch?v=ysdShEL1HMM&t=398s
"""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
# Import the database tables
from model import Dummy

flk_admin = Admin()   # To view the tables contents


class DBAdmin:

    @staticmethod
    def create_admin_views(db):
        flk_admin.add_view(ModelView(Dummy, db.session))

