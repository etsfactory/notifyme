
"""
Users handler
"""
import settings as st

from connectors.rethink import RethinkHandler
from connectors.data_streaming import DataStreaming

from bussiness.db_handler import DBHandler

class BusFilter(object):

    def __init__(self, exchange, key):
        self.exchange = exchange
        self.key = key
        self.exchange_key = [exchange, key]
    
class BusFiltersHandler(object):
    """
    bus_filters handlers class to get, edit, and streaming bus_filters from the database
    """
    def __init__(self):
        self.db_handler = DBHandler("bus_filters")
        self.db_handler.create_table('exchange_key')

    def get_bus_filters(self):
        """
        Get all the bus_filters from the database
        """
        return self.db_handler.get_data()

    def get_bus_filter_streaming(self):
        """
        Get all bus_filters from the database in realtime.
        If user is added or modified in the db it returns the change.
        This method blocks the curren thread so use this method in a separated thread
        """
        return self.db_handler.get_data_streaming()

    def insert_bus_filter(self, bus_filter):
        """
        Insert bus_filter to the database
        """
        return self.db_handler.insert_data(bus_filter)

    def edit_bus_filter(self, bus_filter):
        """
        Modify bus_filter by his email
        """
        self.db_handler.edit_data(bus_filter, 'id', bus_filter.id)

    def get_filter_by_exchange_key(self, exchange_key):
        return self.db_handler.filter_data({'exchange_key': exchange_key})