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
        self.start_connection()

        cursor = self.subscriptions.get_realtime()

        try:
            for subscription in cursor:
                if subscription['old_val']:
                    """
                    When a subscription is deleted
                    """
                    self.on_subscription_delete(subscription['old_val'])
                if subscription['new_val']:
                    print(subscription)
                    """
                    When a subscription is added or edited
                    """
                    self.start_connection()
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
                    self.start_connection()
        except BaseException:
            raise ConnectionLost()

    def start_connection(self):
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
    
    def on_subscription_delete(self, subscription):

        if isinstance(subscription, list):
            for sub in subscription:
                bus_filters = self.bus_filters_from_subsc(sub)
        else:
            bus_filters = self.bus_filters_from_subsc(subscription)

        print(bus_filters)
        if (len(bus_filters) == 1):
            self.connection_stop(bus_filters[0])
    
    def bus_filters_from_subsc(self, subscription):
        bus_filter = self.check_subscription(subscription)
        return self.subscriptions.get_by_filter(bus_filter)

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
            self.bus_thread.set_subscriptions(subscriptions)
        self.bus_thread.start()

    def connection_stop(self, bus_filter):
        """
        Search for a thread with the bus_filter to pause and delete it
        """
        if hasattr(self, 'bus_thread'):
           

            self.bus_thread.stop()
            if bus_filter:
                self.bus_thread.unbind(bus_filter['exchange'], bus_filter['key'])
