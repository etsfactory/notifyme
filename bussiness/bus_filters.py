
"""
Users handler
"""
import settings as st

from connectors.rethink import RethinkHandler
from bussiness.db_handler import DBHandler

class BusFilter(object):
    """
    Bus filter. To filter from the bus with exchange and key
    """

    def __init__(self, exchange, key):
        self.exchange = exchange
        self.key = key
        self.exchange_key = [exchange, key]
    
class BusFiltersHandler(object):
    """
    Bus_filters handlers class to get, edit, and streaming bus_filters from the database
    """
    def __init__(self):
        self.db_handler = DBHandler("bus_filters")
        self.db_handler.create_table('exchange_key')

    def get(self):
        """
        Get all the bus_filters from the database
        """
        return self.to_object(self.db_handler.get_data())

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
        return self.db_handler.insert_data(bus_filter)

    def edit(self, bus_filter):
        """
        Modify bus_filter by his email
        """
        self.db_handler.edit_data(bus_filter, bus_filter.exchange_key, 'exchange_key')

    def delete(self, bus_filter):
        """
        Delete bus_filter by his exchange_key 
        """
        self.db_handler.delete_data(bus_filter.exchange_key)

    def get_by_exchange_key(self, exchange_key):
        """
        Returns exchange searching by his exchange key
        """
        return self.to_object(self.db_handler.filter_data({'exchange_key': exchange_key}))[0]
    
    def to_object(self, data):
        """
        Parse db filter object to Filter instance
        """
        filters = []
        for bus_filter in data:
            filters.append(BusFilter(bus_filter['exchange'], bus_filter['key']))
        return filters