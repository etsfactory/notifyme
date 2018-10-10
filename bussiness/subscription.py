
"""
Users handler
"""
import settings as st

from connectors.rethink import RethinkHandler
from connectors.data_streaming import DataStreaming

from bussiness.db_handler import DBHandler

class Subscription(object):

    def __init__(self, email, exchange, key):
        self.email = email
        self.exchange = exchange
        self.key = key

class SubscriptionHandler(object):
    """
    Subscription type handlers class to get, edit, and streaming subscriptions from the database
    """
    def __init__(self):
        self.db_handler = DBHandler("subscriptions")
        self.db_handler.create_table('id')

    def get_subscription(self):
        """
        Get all the users from the database
        """
        return self.db_handler.join_tables("subscriptions", "users", "notification_types", "email", "exchange")
        
    def get_subscription_streaming(self):
        """
        Get all subscriptions from the database in realtime.
        If user is added or modified in the db it returns the change.
        This method blocks the curren thread so use this method in a separated thread
        """
        return self.db_handler.get_data_streaming()

    def insert_subscription(self, subscription):
        """
        Insert subscriptions to the database
        """
        self.db_handler.insert_data(subscription)

    def edit_subscription(self, subscription):
        """
        Modify subscriptions
        """
        self.db_handler.edit_data(subscription, 'key', subscription.user_id)

