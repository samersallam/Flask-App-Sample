"""
A useful URL
https://www.youtube.com/watch?v=ysdShEL1HMM&t=398s
"""
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

flk_admin = Admin()   # To view the tables contents

# Import the database tables
# from model import User

class DBAdmin:

    @staticmethod
    def create_admin_views(db):
        # flk_admin.add_view(ModelView(User, db.session))
        pass
