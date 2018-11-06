
"""
Users handler
"""
import settings as st

from bussiness.db_handler import DBHandler
from bussiness.subscriptions import SubscriptionsHandler

from marshmallow import Schema, fields


class BusFilterSchema(Schema):
    id = fields.Str()
    exchange = fields.Str(required=True)
    key = fields.Str()


class BusFiltersHandler(object):
    """
    Bus_filters handlers class to get, edit, and streaming bus_filters from the database
    """

    def __init__(self):
        self.db_handler = DBHandler("bus_filters")
        self.db_handler.create_table()
        self.subscriptions = SubscriptionsHandler()

    def get(self, key=None):
        """
        Get all the bus_filters from the database
        """
        return self.db_handler.get_data(key)

    def get_realtime(self):
        """
        Get all bus_filters from the database in realtime.
        If user is added or modified in the db it returns the change.
        This method blocks the curren thread so use this method in a separated thread
        """
        return self.db_handler.get_data_streaming()

    def insert(self, bus_filter):
        """
        Insert bus_filter to the database
        """
        result, errors = BusFilterSchema().load(bus_filter)
        if errors:
            st.logger.error('Bus filter creation error: %s', errors)
        else:
            return self.db_handler.insert_data(result)

    def edit(self, bus_filter, bus_filter_id):
        """
        Modify bus_filter by his email
        """
        self.db_handler.edit_data(bus_filter, bus_filter_id, 'id')

    def delete(self, bus_filter_id):
        """
        Delete bus_filter by his id 
        """
        self.db_handler.delete_data(bus_filter_id)
        self.subscriptions.delete_bus_filter(bus_filter_id)

    def get_by_exchange_key(self, exchange, key):
        """
        Passing an exchange and key searchs in the db for a bus filter 
        """
        return self.db_handler.filter_data({'exchange': exchange, 'key': key})[0]

    def search(self, bus_filter):
        """
        Searchs for a bus filter in a db and returns the id
        """
        bus_filters = self.db_handler.filter_data(
            {'exchange': bus_filter['exchange'], 'key': bus_filter['key']})
        if len(bus_filters) > 0:
            return bus_filters[0]['id'], False
        else:
            return None, True
