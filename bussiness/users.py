
"""
Users handler
"""
import settings as st

from bussiness.db_handler import DBHandler
from marshmallow import Schema, fields


class UserSchema(Schema):
    id = fields.Str()
    name = fields.Str()
    email = fields.Email()


class UsersHandler(object):
    """
    Users handlers class to get, edit, and streaming users from the database
    """

    def __init__(self):
        self.db_handler = DBHandler("users")
        self.db_handler.create_table()

    def get(self, user_id=None):
        """
        Get all the users from the database
        """
        return self.db_handler.get_data(user_id)

    def get_realtime(self):
        """
        Get all users from the database in realtime.
        If user is added or modified in the db it returns the change.
        This method blocks the curren thread so use this method in a separated thread
        """
        return self.db_handler.get_data_streaming()

    def insert(self, user):
        """
        Insert user or users to the database
        """
        result, errors = UserSchema().load(user)
        if errors:
            st.logger.error('User creation error: %s', errors)
        else:
            return self.db_handler.insert_data(result)

    def edit(self, user, user_id):
        """
        Modify user by his id
        """
        self.db_handler.edit_data(user, user_id, 'id')

    def delete(self, user_id):
        self.db_handler.delete_data(user_id)

    def get_by_email(self, email):
        """
        Get user by his email
        """
        users = self.db_handler.filter_data({'email': email})
        if len(users) > 0:
            return users[0]
        else:
            return None

    def search(self, user):
        users = self.db_handler.filter_data(
            {'email': user['email'], 'name': user['name']})
        if len(users) > 0:
            return users[0]['id']
        else:
            return None
