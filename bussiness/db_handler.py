"""
Users handler
"""

import settings as st
import ast

from connectors.rethink import RethinkHandler
from connectors.data_streaming import DataStreaming

import json

class DBHandler(object):
    """
    Users handlers class to get, edit, and streaming users from the database
    """

    def __init__(self, table_name):
        self.db = RethinkHandler(st.DB_SERVER, st.DB_PORT, st.DB_NAME)
        self.db_streaming = DataStreaming(st.DB_SERVER, st.DB_PORT, st.DB_NAME)
        self.table_name = table_name

    def create_table(self, primary_key='id'):
        """
        Creates the table in database and regenerates if it already exists
        """
        self.db.create_table(self.table_name, primary_key=primary_key)

    def get_data(self):
        """
        Get data from the database
        """
        return self.db.get_data(self.table_name)

    def get_data_streaming(self):
        """
        Get data from the database in realtime.
        If data is added or modified in the db it returns the change.
        This method blocks the current thread so use this method in a separated thread
        """
        return self.db_streaming.get_data(self.table_name)

    def insert_data(self, data):
        """
        Inserts data into the database
        """
        self.db.insert_data(self.table_name, self.convert_to_json_list(data))

    def edit_data(self, data, key, key_value, primary_key ='id'):
        """
        Modifies data 
        """
        entries = self.db.filter_data(self.table_name, {key: key_value})
        for document in entries:
           self.db.edit_data(self.table_name, document[primary_key], self.convert_to_json(data))

    def filter_data(self, data):
        """
        Filters data from the database
        """
        self.db.filter_data(self.table_name, data)  
    
    def convert_to_json_list(self, data): 
        """
        Converts list of objects to json list 
        """
        entry = json.dumps([data.__dict__])
        return ast.literal_eval(entry)

    def convert_to_json(self, data): 
        """
        Converts list of objects to json list 
        """
        entry = json.dumps(data.__dict__)
        return ast.literal_eval(entry)