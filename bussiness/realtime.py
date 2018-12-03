"""
Realtime module
"""
from threading import Thread

from exceptions.db_exceptions import ConnectionLost

from bussiness.bus_connection import BusConnectionHandler

from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionsHandler
from bussiness.templates import TemplatesHandler


class Realtime():
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
        Realtime subscriptions.
        If a subscription is removed, the bus connection stops
        If a subscription is updated, recreates the thread
        """
        self.start_connection()

        cursor = self.subscriptions.get_realtime()

        try:
            for subscription in cursor:
                if subscription['old_val'] and not subscription['new_val']:
                    # When a subscription is deleted
                    self.on_subscription_delete(subscription['old_val'])
                if subscription['new_val'] and not subscription['new_val']:
                    # When a subscription is added
                    self.start_connection()
        except BaseException:
            raise ConnectionLost()

    def realtime_filters(self):
        """
        Realtime bus filters. Listening for a template
        change in the database.
        """
        cursor = self.filters.get_realtime()
        try:
            for bus_filter in cursor:
                if bus_filter['old_val'] and not bus_filter['new_val']:
                    # When a bus filter is deleted
                    self.on_bus_filter_delete(bus_filter['old_val'])
               # if bus_filter['new_val'] and bus_filter['old_val']:
                    # When a bus filter is edited
               #     self.start_connection()
        except BaseException:
            raise ConnectionLost()

    def realtime_templates(self):
        """
        Realtime templates. Listening for a template
        change in the database.
        """
        cursor = self.templates.get_realtime()
        try:
            for template in cursor:
                if template['old_val'] and not template['new_val']:
                    template_id = template['old_val'].get('id')
                    self.filters.delete_template(template_id)
                    subscriptions = self.subscriptions.subscriptions_template(template_id)
                    for subscription in subscriptions:
                        del subscription['template_id']
                        edited_subscription = self.subscriptions.set_subscription_template(
                            subscription)
                        self.subscriptions.edit(
                            edited_subscription, edited_subscription['id'])

        except BaseException:
            raise ConnectionLost()

    def start_connection(self):
        """
        Creates a new connection thread listening
        to the subscriptions stored in the database
        """
        bus_filters = []
        subscriptions_list = self.subscriptions.get()
        if subscriptions_list:
            for sub in subscriptions_list:
                bus_filters.append(self.bus_filter_from_subscription(sub))
            if bus_filters:
                self.create_connection(bus_filters)

    def bus_filter_from_subscription(self, subscription):
        """
        Returns bus filters with the same bus filter id
        than the subscription bus filter
        :subscription: Subscription that is going to look for bus filters
        """
        return self.filters.get(subscription.get('filter_id'))

    def on_subscription_delete(self, subscription):
        """
        If a subscription is deleted, it search if is the
        last subscription with this bus filters. If so, it
        stops listen to this bus filter from the bus
        """
        subscriptions = []
        if isinstance(subscription, list):
            for sub in subscription:
                subscriptions = subscriptions + \
                    self.same_bus_filter_subscription(sub)
        else:
            subscriptions = self.same_bus_filter_subscription(subscription)

        if subscriptions:
            if len(subscriptions) == 1:
                # If only one subscription left, unbind bus filter
                bus_filter = self.bus_filter_from_subscription(subscription)
                self.connection_stop(bus_filter)

    def same_bus_filter_subscription(self, subscription):
        """
        Returns all subscriptions with the same
        bus filter than the provided subscription
        :subscription: Subscription that is going to look for bus filters
        """
        try:
            return self.subscriptions.get_by_filter_id(
                subscription.get('filter_id'))
        except BaseException:
            pass

    def on_bus_filter_delete(self, bus_filter):
        """
        If a bus filter is delete, delete it from
        the subscriptions asociated to and stops
        listening from the bus
        """
        self.subscriptions.delete_bus_filter(bus_filter)
        self.connection_stop(bus_filter)

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

    def connection_stop(self, bus_filter=None):
        """
        Search for a thread with the bus_filter to pause and delete it
        """
        if hasattr(self, 'bus_thread'):
            self.bus_thread.stop()
            if bus_filter:
                self.bus_thread.unbind(
                    bus_filter.get('exchange'),
                    bus_filter.get('key'))
