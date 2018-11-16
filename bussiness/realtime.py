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

    def realtime_subscriptions(self):
        """
        Realtime filters. Creates a thread per new change
        to listen for a exchange and key in the bus.
        If a filter is removed, the bus connection stops listening and the thread is stopped
        If a filter is updated, the thread stops and creates and new thread
        """
        subs = self.subscriptions.get()
        if subs:
            self.on_subscription_added(subs)

        cursor = self.subscriptions.get_realtime()

        try:
            for subscription in cursor:
                if not subscription['new_val']:
                    """
                    When a subscription is deleted
                    """
                    self.thread_stop()
                if subscription['new_val']:
                    """
                    When a subscription is added or edited
                    """
                    self.on_subscription_added(subscription['new_val'])
        except ConnectionLost:
            raise

    def on_subscription_added(self, subscription):
        """
        Subscriptions added. Creates a new connection thread
        """
        subscriptions = []
        if isinstance(subscription, list):
            for sub in subscription:
                subscriptions = subscriptions + self.check_subscription(sub)
        else:
            subscriptions = subscriptions + self.check_subscription(subscription)
        
        self.thread_stop()
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
            self.bus_thread.set_subscriptions(subscriptions)
        self.bus_thread.start()

    def thread_stop(self):
        """
        Search for a thread with the bus_filter to pause and delete it
        """
        if hasattr(self, 'bus_tread'):
            self.bus_thread.stop()
