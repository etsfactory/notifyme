
"""
Users handler
"""
import settings as st

from connectors.rethink import RethinkHandler
from bussiness.db_handler import DBHandler

from marshmallow import Schema, fields, pprint

class BusFilterSchema(Schema):
    id = fields.Str()
    exchange = fields.Str()
    key = fields.Str()

class BusFilter(object):
    """
    Bus filter. To filter from the bus with exchange and key
    """

    def __init__(self, exchange, key, id=None):
        self.exchange = exchange
        self.key = key
        if id:
            self.id = id
    
class BusFiltersHandler(object):
    """
    Bus_filters handlers class to get, edit, and streaming bus_filters from the database
    """
    def __init__(self):
        self.db_handler = DBHandler("bus_filters")
        self.db_handler.create_table()

    def get(self, key=None):
        """
        Get all the bus_filters from the database
        """
        return self.to_object(self.db_handler.get_data(key))

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

    def edit(self, bus_filter, bus_filter_id):
        """
        Modify bus_filter by his email
        """
        self.db_handler.edit_data(bus_filter, bus_filter_id, 'id')

    def delete(self, bus_filter):
        """
        Delete bus_filter by his id 
        """
        self.db_handler.delete_data(bus_filter.id)
    
    def search(self, bus_filter):
        bus_filters = self.db_handler.filter_data({'exchange': bus_filter.exchange, 'key': bus_filter.key})
        if len(bus_filters) > 0:
            return bus_filters[0]['id'], False
        else:
            return None, True

    def to_object(self, data):
        """
        Parse db filter object to Filter instance. If the data provided is an array, 
        returns an array of Filter instances
        """
        filters = []
        if isinstance(data, dict):
            return BusFilter(data['exchange'], data['key'], data['id'])
        else: 
            for bus_filter in data:
                exchange = bus_filter['exchange']
                key = bus_filter['key']
                bus_id =  bus_filter['id']
                filters.append(BusFilter(exchange, key, bus_id))
            return filters

            
        
