
"""
Users handler
"""
import settings as st

from connectors.rethink import RethinkHandler
from bussiness.db_handler import DBHandler

class User(object):

    def __init__(self, name, email):
        self.name = name
        self.email = email

class UsersHandler(object):
    """
    Users handlers class to get, edit, and streaming users from the database
    """
    def __init__(self):
        self.db_handler = DBHandler("users")
        self.db_handler.create_table('email')

    def get(self):
        """
        Get all the users from the database
        """
        return self.to_object(self.db_handler.get_data())

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
        self.db_handler.insert_data(user)

    def edit(self, user):
        """
        Modify user by his email
        """
        self.db_handler.edit_data(user, user.email, 'email')
    
    def delete(self, user):
        self.db_handler.delete_data(user.email)
    
    def get_by_email(self, email):
        """
        Get user by his email
        """
        return self.to_object(self.db_handler.filter_data({'email': email}))[0]
     
    def to_object(self, data):
        """
        Parse db user object to User instance
        """
        users = []
        for user in data:
            users.append(User(user['name'], user['email']))
        return users
        