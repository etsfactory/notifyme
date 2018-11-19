"""
Users handler
"""
import ast

import settings as st
import utils.json_parser as json_parser
from connectors.rethink import RethinkHandler
from connectors.rethink_realtime import BDRealtime
from exceptions.db_exceptions import WriteError, ReadError

recreate_database = st.REFRESH_DATABASE


class DBHandler(object):
    """
    Users handlers class to get, edit, and streaming users from the database
    """

    def __init__(self, table_name):
        self.db = RethinkHandler(
            st.DB_SERVER, st.DB_PORT, st.DB_NAME, st.DB_USER, st.DB_PASSWORD)
        self.db_realtime = BDRealtime(st.DB_SERVER, st.DB_PORT, st.DB_NAME)
        self.table_name = table_name

    def create_table(self, primary_key='id'):
        """
        Creates the table in database and regenerates if it already exists
        """
        global recreate_database
        if (recreate_database):
            self.db.reset_database()
            st.logger.info('Reseting the database...')
            recreate_database = False
        else:
            self.db.create_table(self.table_name, primary_key)

    def get_data(self, key=None):
        """
        Get data from the database
        """
        data = self.db.get_data(self.table_name, key)
        if (not key):
            data_list = []
            for entry in data:
                data_list.append(entry)
            return data_list
        else:
            return data

    def get_data_streaming(self):
        """
        Get data from the database in realtime.
        If data is added or modified in the db it returns the change.
        This method blocks the current thread so use this method in a separated thread
        """
        return self.db_realtime.get_data(self.table_name)

    def insert_data(self, data):
        """
        Inserts data into the database
        """
        return self.db.insert_data(self.table_name, data)

    def edit_data(self, data, key_value, key='id'):
        """
        Modifies data 
        """
        entries = self.filter_data({key: key_value})
        for document in entries:
            return self.db.edit_data(
                self.table_name, document[key], data)

    def delete_data(self, key_value):
        self.db.delete_data(self.table_name, key_value)

    def filter_data(self, filter):
        """
        Filters data from the database
        """
        data = self.db.filter_data(self.table_name, filter)
        data_list = []
        for entry in data:
            data_list.append(entry)
        return data_list

    def join_tables(self, table1, table2, table3, key1, key2):
        """
        Joins two tables
        :table1: Table with the foreign keys
        :table2: Lelft table to join
        :table3: Right table to join
        :key1: Foering key from the left table
        :key2: Foering key for the right table
        """

        return self.db.join_tables(table1, table2, table3, key1, key2)

    def table_join_streaming(self, table1, table2, table3, key1, key2):
        return self.db_realtime.table_join_streaming(table1, table2, table3, key1, key2)
