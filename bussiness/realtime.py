"""
Realtime module
"""
import time
from threading import Thread

import settings as st
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionsHandler
from bussiness.templates import TemplatesHandler

from bussiness.bus_connection import BusConnectionHandler
from connectors.smtp import SMTPHandler

from exceptions.db_exceptions import ConnectionLost


class Realtime(object):
    """
    Realtime class
    """

    def __init__(self):
        self.filters = BusFiltersHandler()
        self.subscriptions = SubscriptionsHandler()
        self.templates = TemplatesHandler()
        Thread(target=self.realtime_subscriptions).start()
        Thread(target=self.realtime_filters).start()

    def realtime_subscriptions(self):
        """
        Realtime filters. Creates a thread per new change
        to listen for a exchange and key in the bus.
        If a filter is removed, the bus connection stops listening and the thread is stopped
        If a filter is updated, the thread stops and creates and new thread
        """
        self.connection_start()

        cursor = self.subscriptions.get_realtime()

        try:
            for subscription in cursor:
                if not subscription['new_val']:
                    """
                    When a subscription is deleted
                    """
                    self.connection_stop()
                if subscription['new_val']:
                    """
                    When a subscription is added or edited
                    """
                    self.connection_start()
        except:
            raise ConnectionLost()

    def realtime_filters(self):
        """
        Realtime filters. Creates a thread per new change
        to listen for a exchange and key in the bus.
        If a filter is removed, the bus connection stops listening and the thread is stopped
        If a filter is updated, the thread stops and creates and new thread
        """
        cursor = self.filters.get_realtime()
        try:
            for bus_filter in cursor:
                if bus_filter['new_val'] and bus_filter['old_val']:
                    """
                    When a subscription is edited
                    """
                    self.connection_start()
        except:
            raise ConnectionLost()

    def connection_start(self):
        """
        Subscriptions added. Creates a new connection thread
        """
        subscriptions = []
        subscriptions_list = self.subscriptions.get()
        for sub in subscriptions_list:
            subscriptions = subscriptions + self.check_subscription(sub)
        if subscriptions:
            self.create_connection(subscriptions)

    def check_subscription(self, subscription):
        subscriptions = []
        bus_filter = self.filters.get(subscription['filter_id'])
        for sub in self.subscriptions.get_with_relationships():
            if sub['filter_id'] == bus_filter['id']:
                subscriptions.append(sub)
        return subscriptions

    def create_connection(self, subscriptions):
        """
        Creates a thread with a new rabbitmq connection
        """
        if not hasattr(self, 'bus_tread'):
            self.bus_thread = BusConnectionHandler(subscriptions)
        else:
            self.connection_stop()
            self.bus_thread.set_subscriptions(subscriptions)
        self.bus_thread.start()

    def connection_stop(self):
        """
        Search for a thread with the bus_filter to pause and delete it
        """
        if hasattr(self, 'bus_thread'):
            self.bus_thread.stop()
