
"""
Users handler
"""
from marshmallow import Schema, fields

from bussiness.db_handler import DBHandler


class UserSchema(Schema):
    """
    User s
    """
    id = fields.Str()
    name = fields.Str()
    email = fields.Email()


class UsersHandler():
    """
    Users handlers class to get, edit, and streaming
    users from the database
    """

    def __init__(self):
        self.db_handler = DBHandler("users")
        self.db_handler.create_table()

    def get(self, user_id=None):
        """
        Get all the users from the database
        :user_id: User id to search for if provided
        """
        return self.db_handler.get_data(user_id)

    def get_realtime(self):
        """
        Get all users from the database in realtime.
        If user is edited in the db it returns the change.
        This method blocks the curren thread
        use this method in a separated thread
        """
        return self.db_handler.get_data_streaming()

    def insert(self, user):
        """
        Insert user or users to the database
        :user: User or users to insert
        """
        return self.db_handler.insert_data(user)

    def edit(self, user, user_id):
        """
        Modify user by his id
        :user: User modified
        :user_id: User id to search for
        """
        self.db_handler.edit_data(user, user_id)

    def delete(self, user_id):
        """
        Delete user from the database
        """
        self.db_handler.delete_data(user_id)

    def get_by_email(self, email):
        """
        Get user by his email
        :email: Email to search for
        """
        users = self.db_handler.filter_data({'email': email})
        if users:
            return users[0]
        return None

    def search(self, user):
        """
        Search user with user provided. Return his id
        :user: User to search for without id
        """
        users = self.db_handler.filter_data(
            {'email': user['email'], 'name': user['name']})
        if users:
            return users[0]['id']
        return None
