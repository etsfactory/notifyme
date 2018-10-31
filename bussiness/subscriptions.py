
"""
Users handler
"""
import settings as st

from connectors.rethink import RethinkHandler
from bussiness.db_handler import DBHandler
from bussiness.users import UsersHandler
from bussiness.bus_filters import BusFiltersHandler
from bussiness.templates import TemplatesHandler

from marshmallow import Schema, fields, pprint

class SubscriptionSchema(Schema):
    id = fields.Str()
    user_id = fields.Str()
    filter_id = fields.Str()
    template_id: fields.Str()

class Subscription(object):

    def __init__(self, user_id, filter_id, template_id=None, id=None):
        self.user_id = user_id
        self.filter_id = filter_id
        self.template_id = template_id
        if id:
            self.id = id

class SubscriptionsHandler(object):
    """
    Subscription type handlers class to get, edit, and streaming subscriptions from the database
    """

    def __init__(self):
        self.db_handler = DBHandler('subscriptions')
        self.db_handler.create_table('id')
        self.users = UsersHandler()
        self.filters = BusFiltersHandler()
        self.templates = TemplatesHandler()

    def get(self, sub_id=None):
        """
        Get all the subscriptions from the database. If id is provided search for a single subscription
        """
        return self.to_object(self.db_handler.get_data(sub_id))

    def get_with_relationships(self):
        """
        Get subscriptions joining users and bus_filtes tables
        """
        return self.db_handler.join_tables("subscriptions", "users", "bus_filters", "user_id", "filter_id")

    def get_realtime(self):
        """
        Get all subscriptions from the database in realtime.
        If user is added or modified in the db it returns the change.
        This method blocks the curren thread so use this method in a separated thread
        """
        return self.db_handler.get_data_streaming()

    def get_users_by_filter(self, bus_filter):
        """
        Get user associates with filter
        """
        users = []
        subscriptions = self.get_by_filter(bus_filter)
        for subscription in subscriptions:
            user = (self.users.get(subscription.user_id))
            users.append(user)
        return users
    
    def get_filters_by_user(self, user):
        """
        Get filters associates with user
        """
        filters = []
        subscriptions = self.get_by_user(user)
        for subscription in subscriptions:
            bus_filter = self.filters.get(subscription.filter_id)
            filters.append(bus_filter)
        return filters

    def get_by_id(self, subsc_id):
        """
        Get subscription by his id
        """
        return self.db_handler.filter_data({'id': subsc_id})
     
    def get_by_filter(self, bus_filter):
        """
        Get subscription by his id
        """
        return self.to_object(self.db_handler.filter_data({'filter_id': bus_filter.id}))
    
    def get_by_user(self, user):
        """
        Get subscription by his id
        """
        return self.to_object(self.db_handler.filter_data({'user_id': user.id}))

    def insert(self, subscription):
        """
        Insert subscriptions to the database
        """
        bus_filter = self.filters.get(subscription.filter_id)
        
        if subscription.template_id:
             subscription.template_id = subscription.template_id
        elif hasattr(bus_filter, 'template_id'):
            subscription.template_id = bus_filter.template_id
        elif (not self.templates.default_template_id):
            self.templates.create_default()
            subscription.template_id = self.templates.default_template_id

        return self.db_handler.insert_data(subscription)

    def edit(self, subscription, subscription_id):
        """
        Modify subscriptions
        """
        self.db_handler.edit_data(subscription, subscription_id, 'id')

    def delete(self, subscription):
        """
        Delete subscription. If no id is pased it will search it 
        """
        self.db_handler.delete_data(subscription.id)
        
    def to_object(self, data):
        """
        Parse db subscription object to Subscription instance
        """
        subs = []
        if isinstance(data, dict):
            return Subscription(data['user_id'], data['filter_id'], data['template_id'], data['id'])
        else:
            for sub in data:
                subs.append(Subscription(sub['user_id'], sub['filter_id'], sub['template_id'], sub['id']))
            return subs