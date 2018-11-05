
"""
Users handler
"""
import settings as st

from connectors.rethink import RethinkHandler
from bussiness.db_handler import DBHandler
import utils.json_parser as json_parser

from marshmallow import Schema, fields, pprint

class BusFilterSchema(Schema):
    id = fields.Str()
    exchange = fields.Str()
    key = fields.Str()
    

class BusFilter(object):
    """
    Bus filter. To filter from the bus with exchange and key
    """
    def __init__(self, exchange, key, template_id=None, id=None):
        self.exchange = exchange
        self.key = key
        if template_id:
            self.template_id = template_id
        if id:
            self.id = id
    
    def set_template(self, template_id):
        self.template_id = template_id
    
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

    def get_by_exchange_key(self, exchange, key):
        """
        Passing an exchange and key searchs in the db for a bus filter 
        """
        return self.to_object(self.db_handler.filter_data({'exchange': exchange, 'key': key})[0])
    
    def search(self, bus_filter):
        """
        Searchs for a bus filter in a db and returns the id
        """
        bus_filters = self.db_handler.filter_data({'exchange': bus_filter.exchange, 'key': bus_filter.key})
        if len(bus_filters) > 0:
            return bus_filters[0]['id'], False
        else:
            return None, True

    def to_object(self, data):
        """
        Parse db filter object to bus filter instance. If the data provided is an array, 
        returns an array of bus filter instances
        """
        if (not data):
            return None
        filters = []
        if isinstance(data, dict):
           return self.create_from_dictionary(data)
        if data: 
            for bus_filter in data:
               filters.append(self.create_from_dictionary(bus_filter))
            return filters
        else:
            return None

    def create_from_dictionary(self, dictionary):
        """
        Creates bus filter instance from dictionary
        """
        exchange = json_parser.dict_keys(dictionary, 'exchange')
        key = json_parser.dict_keys(dictionary, 'key')
        template = json_parser.dict_keys(dictionary, 'template_id')
        bus_id =  json_parser.dict_keys(dictionary, 'id')
        return BusFilter(exchange, key, template, bus_id)
            
