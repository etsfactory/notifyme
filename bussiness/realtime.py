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
        Thread(target=self.realtime_templates).start()

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
                if subscription['old_val'] and not subscription['new_val']:
                    """
                    When a subscription is deleted
                    """
                    self.on_subscription_delete(subscription['old_val'])
                if subscription['new_val'] and not subscription['new_val']:
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
                if bus_filter['old_val'] and not bus_filter['new_val']:
                    self.on_bus_filter_delete(bus_filter['old_val'])
                if bus_filter['new_val'] and bus_filter['old_val']:
                    """
                    When a subscription is edited
                    """
                    self.start_connection()
        except BaseException:
            raise ConnectionLost()
    
    def realtime_templates(self):

        cursor = self.templates.get_realtime()
        try:
            for template in cursor:
                if template['old_val'] and not template['new_val']:
                    self.filters.delete_template(template['old_val']['id'])
                    subscriptions = self.subscriptions.subscriptions_template(template['old_val']['id'])
                    for subscription in subscriptions:
                        del subscription['template_id']
                        edited_subscription = self.subscriptions.set_subscription_template(subscription)
                        self.subscriptions.edit(edited_subscription, edited_subscription['id'])
               
        except BaseException:
            raise ConnectionLost()

    def start_connection(self):
        """
        Subscriptions added. Creates a new connection thread
        """
        bus_filters = []
        subscriptions_list = self.subscriptions.get()
        print(subscriptions_list)
        if (len(subscriptions_list) > 0):
            for sub in subscriptions_list:
                bus_filters.append(self.check_subscription(sub))
            if len(bus_filters) > 0:
                self.create_connection(bus_filters)

    def on_bus_filter_delete(self, bus_filter):
        self.subscriptions.delete_bus_filter(bus_filter)
        self.connection_stop(bus_filter)
    
    def on_subscription_delete(self, subscription):
        subscriptions = []
        if isinstance(subscription, list):
            for sub in subscription:
                subscriptions = subscriptions + self.bus_filters_from_subsc(sub)
        else:
            subscriptions = self.bus_filters_from_subsc(subscription)

        if subscriptions:
            if (len(subscriptions) < 1):
                bus_filter = self.check_subscription(subscription)
                self.connection_stop(bus_filter)
    
    def bus_filters_from_subsc(self, subscription):
        try:
            return self.subscriptions.get_by_filter_id(subscription.get('filter_id'))
        except: 
            pass

    def check_subscription(self, subscription):
        """
        Returns bus filters with the same bus filter id 
        than the subscription bus filter
        :subscription: Subscription that is going to look for bus filters
        """
        print(subscription)
        return self.filters.get(subscription.get('filter_id'))

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
                self.bus_thread.unbind(bus_filter.get('exchange'), bus_filter.get('key'))
