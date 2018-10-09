"""
Users handler
"""

import settings as st

from connectors.rethink import RethinkHandler
from connectors.data_streaming import DataStreaming

class UsersHandler(object):
    """
    Users handlers class to get, edit, and streaming users from the database
    """
    table_name = "users"

    def __init__(self):
        self.db = RethinkHandler(st.DB_SERVER, st.DB_PORT, st.DB_NAME)
        self.db_streaming = DataStreaming(st.DB_SERVER, st.DB_PORT, st.DB_NAME)
        self.create_table()

    def create_table(self):
        """
        Creates table in the database and regenerates it if the table exists
        """
        self.db.create_table(self.table_name, primary_key='id')

    def get_users(self):
        """
        Get all the users from the database
        """
        return self.db.get_data(self.table_name)

    def get_users_streaming(self):
        """
        Get all users from the database in realtime.
        If user is added or modified in the db it returns the change.
        This method blocks the curren thread so use this method in a separated thread
        """
        return self.db_streaming.get_data(self.table_name)

    def insert_user(self, data):
        """
        Insert user or users to the database
        """
        self.db.insert_data(self.table_name, data)

    def edit_user(self, params):
        """
        Modify user by his email
        """
        user = self.db.filter_data(self.table_name, {'email': params['email']})
        for document in user:
            self.db.edit_data(self.table_name, document['id'], params)
