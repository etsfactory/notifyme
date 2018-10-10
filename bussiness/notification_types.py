
"""
Users handler
"""
import settings as st

from connectors.rethink import RethinkHandler
from connectors.data_streaming import DataStreaming

from bussiness.db_handler import DBHandler

class NotificationType(object):

    def __init__(self, exchange, key):
        self.exchange = exchange
        self.key = key
    

class NotificationTypeHandler(object):
    """
    Notification type handlers class to get, edit, and streaming notification types from the database
    """
    def __init__(self):
        self.db_handler = DBHandler("notification_types")
        self.db_handler.create_table('exchange')

    def get_notification_type(self):
        """
        Get all the users from the database
        """
        return self.db_handler.get_data()

    def get_notification_type_streaming(self):
        """
        Get all users from the database in realtime.
        If user is added or modified in the db it returns the change.
        This method blocks the curren thread so use this method in a separated thread
        """
        return self.db_handler.get_data_streaming()

    def insert_notification_type(self, notification_type):
        """
        Insert user or users to the database
        """
        self.db_handler.insert_data(notification_type)

    def edit_notification_type(self, notification_type):
        """
        Modify user by his email
        """
        self.db_handler.edit_data(notification_type, 'key', notification_type.key)

