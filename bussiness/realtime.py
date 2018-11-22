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
        If a filter is removed, the bus connection stops
        If a filter is updated, recreates the thread
        """
        self.connection_start()

        cursor = self.subscriptions.get_realtime()

        try:
            for subscription in cursor:
                if not subscription['new_val']:
                    """
                    When a subscription is deleted
                    """
                    # self.connection_stop()
                if subscription['new_val']:
                    print(subscription)
                    """
                    When a subscription is added or edited
                    """
                    # self.connection_start()
        except BaseException:
            raise ConnectionLost()

    def realtime_filters(self):
        """
        Realtime filters. Creates a thread per new change
        to listen for a exchange and key in the bus.
        If a filter is updated, the thread is recreated
        """
        cursor = self.filters.get_realtime()
        try:
            for bus_filter in cursor:
                if bus_filter['new_val'] and bus_filter['old_val']:
                    """
                    When a subscription is edited
                    """
                    self.connection_start()
        except BaseException:
            raise ConnectionLost()

    def connection_start(self):
        """
        Subscriptions added. Creates a new connection thread
        """
        bus_filters = []
        subscriptions_list = self.subscriptions.get()
        if (len(subscriptions_list) > 0):
            for sub in subscriptions_list:
                bus_filters.append(self.check_subscription(sub))
            if len(bus_filters) > 0:
                self.create_connection(bus_filters)
            else:
                self.connection_stop()

    def check_subscription(self, subscription):
        """
        Returns bus filters with the same bus filter id 
        than the subscription bus filter
        :subscription: Subscription that is going to look for bus filters
        """
        return self.filters.get(subscription['filter_id'])

    def create_connection(self, subscriptions):
        """
        Creates a thread with a new rabbitmq connection
        :subscriptions: Subscriptions to add to bus thread
        """
        if not hasattr(self, 'bus_thread'):
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
