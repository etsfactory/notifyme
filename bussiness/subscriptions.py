
"""
Users handler
"""
import settings as st

from bussiness.db_handler import DBHandler
from bussiness.users import UsersHandler
from bussiness.bus_filters import BusFiltersHandler
from bussiness.templates import TemplatesHandler

from marshmallow import Schema, fields


class SubscriptionSchema(Schema):
    id = fields.Str()
    user_id = fields.Str(required=True)
    filter_id = fields.Str(required=True)
    template_id = fields.Str()


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
        return self.db_handler.get_data(sub_id)

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
            user = (self.users.get(subscription['user_id']))
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
        return self.db_handler.filter_data({'filter_id': bus_filter['id']})

    def get_by_user(self, user):
        """
        Get subscription by his id
        """
        return self.db_handler.filter_data({'user_id': user['id']})

    def insert(self, subscriptions):
        """
        Insert subscriptions to the database
        """
        if (isinstance(subscriptions, list)):
            for sub in subscriptions:
                sub = self.set_subscription_template(sub)
        else:
            subscriptions = self.set_subscription_template(subscriptions)
        return self.db_handler.insert_data(subscriptions)

    def set_subscription_template(self, subscription):

        bus_filter = self.filters.get(subscription['filter_id'])

        if not hasattr(subscription, 'template_id') and hasattr(bus_filter, 'template_id'):
            subscription['template_id'] = bus_filter['template_id']
        else:
            subscription['template_id'] = self.templates.get_default_template()
        return subscription

    def edit(self, subscription, subscription_id):
        """
        Modify subscriptions
        """
        self.db_handler.edit_data(subscription, subscription_id, 'id')

    def delete_user(self, user_id):
        subscriptions = self.get()
        for sub in subscriptions:
            if sub['user_id'] == user_id:
                self.delete(sub['id'])

    def delete_bus_filter(self, bus_filter_id):
        subscriptions = self.get()
        for sub in subscriptions:
            if sub['filter_id'] == bus_filter_id:
                self.delete(sub['id'])

    def delete(self, subscription_id):
        """
        Delete subscription.
        """
        self.db_handler.delete_data(subscription_id)
