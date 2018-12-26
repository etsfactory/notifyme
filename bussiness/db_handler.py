"""
Users handler
"""
import settings as st
from connectors.rethink import RethinkHandler
from connectors.rethink_realtime import BDRealtime

recreate_database = st.REFRESH_DATABASE


class DBHandler():
    """
    Users handlers class to get, edit, and streaming
    users from the database
    """

    def __init__(self, table_name):
        self.database = RethinkHandler(
            st.DB_SERVER, st.DB_PORT, st.DB_NAME, st.DB_USER, st.DB_PASSWORD)
        self.db_realtime = BDRealtime(st.DB_SERVER, st.DB_PORT, st.DB_NAME)
        self.table_name = table_name

    def create_table(self, primary_key='id'):
        """
        Creates the table in database
        regenerates if it already exists
        :primary_key: Name of the primary key to create
        """
        global recreate_database
        if recreate_database:
            self.database.reset_database()
            st.logger.info('Reseting the database...')
            recreate_database = False
        else:
            self.database.create_table(self.table_name, primary_key)

    def get_data(self, key=None):
        """
        Get data from the database
        :key: If key is passed it searchs in the database
        """
        data = self.database.get_data(self.table_name, key)
        if not key:
            data_list = []
            for entry in data:
                data_list.append(entry)
            return data_list
        return data

    def get_data_streaming(self):
        """
        Get data from the database in realtime.
        If data is edited in the database it returns the change.
        This method blocks the current thread
        use this method in a separated thread
        """
        return self.db_realtime.get_data(self.table_name)

    def insert_data(self, data):
        """
        Inserts data into the database
        :data: Data to insert, object or array
        """
        result = self.database.insert_data(
            self.table_name, data)
        if isinstance(data, list):
            if data[0].get('id'):
                return [d['id'] for d in data]
        else:
            if data.get('id'):
                return [data.get('id')]
        return result.get('generated_keys')

    def edit_data(self, data, key_value):
        """
        Modifies data
        :data: Edited data to replace
        :key_value: The name of the primary key param
        :key: The key value of the data to edit
        """
        return self.database.edit_data(
            self.table_name, key_value, data)

    def replace_data(self, data, key_value):
        """
        Replaces data
        :data: Edited data to replace
        :key_value: The name of the primary key param
        :key: The key value of the data to edit
        """
        return self.database.replace_data(
            self.table_name, data, key_value)

    def delete_data(self, key_value):
        """
        Delete data from the database
        :key_value: The value of the primary key to delete
        """
        self.database.delete_data(self.table_name, key_value)

    def filter_data(self, filter_params):
        """
        Filters data from the database
        :filter: Object with the filter to use in the database
        """
        data = self.database.filter_data(self.table_name, filter_params)
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

        return self.database.join_tables(table1, table2, table3, key1, key2)
