
"""
Users handler
"""
import settings as st

from connectors.rethink import RethinkHandler
from bussiness.db_handler import DBHandler
from bussiness.users import UsersHandler
from bussiness.bus_filters import BusFiltersHandler

class Subscription(object):

    def __init__(self, email, filter_id):
        self.email = email
        self.filter_id = filter_id

class SubscriptionHandler(object):
    """
    Subscription type handlers class to get, edit, and streaming subscriptions from the database
    """

    def __init__(self):
        self.db_handler = DBHandler('subscriptions')
        self.db_handler.create_table('id')
        self.users = UsersHandler()
        self.filters = BusFiltersHandler()

    def get(self, sub_id):
        """
        Get all the subscriptions from the database. If id is provided search for a single subscription
        """
        return self.to_object(self.db_handler.get_data(sub_id))

    def get_with_relationships(self):
        """
        Get subscriptions joining users and bus_filtes tables
        """
        return self.db_handler.join_tables("subscriptions", "users", "bus_filters", "email", "exchange")

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
            email = subscription['email']
            user = (self.users.get_by_email(email))
            users.append(user)
        return users
    
    def get_filters_by_user(self, user):
        """
        Get filters associates with user
        """
        filters = []
        subscriptions = self.get_by_user(user)
        for subscription in subscriptions:
            bus_filter = self.filters.get(subscription['filter_id'])
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
        return self.db_handler.filter_data({'filter_id': bus_filter.id})
     
    def get_by_user(self, user):
        """
        Get subscription by his id
        """
        return self.db_handler.filter_data({'email': user.email})

    def insert(self, subscription):
        """
        Insert subscriptions to the database
        """
        self.db_handler.insert_data(subscription)

    def edit(self, subscription):
        """
        Modify subscriptions
        """
        self.db_handler.edit_data(subscription, subscription.id)

    def delete(self, subscription):
        """
        Delete subscription. If no id is pased it will search it 
        """
        if hasattr(subscription, 'id'):
            self.db_handler.delete_data(subscription.id)
        else:
            subscriptions = self.db_handler.get_data()
            for sub in subscriptions:
                if sub['email'] == subscription.email and sub['filter_id'] == subscription.filter_id:
                    self.db_handler.delete_data(sub['id'])


    def to_object(self, data):
        """
        Parse db subscription object to Subscription instance
        """
        subscriptions = []
        for subs in data:
            subscriptions.append(Subscription(subs['email'], subs['filter_id']))
        return subscriptions