"""
Realtime module
"""
import time
from threading import Thread

import settings as st
from bussiness.bus_filters import BusFilter
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionsHandler
from bussiness.subscriptions import Subscription
from bussiness.bus_connection import BusConnectionHandler
from connectors.smtp import SMTPHandler

class Realtime(object):
    """
    Realtime class
    """
    def __init__(self):
        self.threads = []
        filters = BusFiltersHandler()
        subscriptions = SubscriptionsHandler()
        Thread(target=self.realtime_filters, args=(filters, subscriptions)).start()

    def realtime_filters(self, filters, subscriptions):
        """
        Realtime filters. Creates a thread per new change
        to listen for a exchange and key in the bus.
        If a filter is removed, the bus connection stops listening and the thread is stopped
        If a filter is updated, the thread stops and creates and new thread
        """
        cursor = subscriptions.get_realtime()
        smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)

        for subscription in cursor:
            st.logger.info(subscription)
            parsed_subscription = self.parse_subscription(subscription)
            if subscription['old_val']:
                """
                When a subscription is deleted
                """
                self.on_subscription_deleted(parsed_subscription)
            if subscription['new_val']:
                """
                When a subscription is added or edited
                """
                self.on_subscription_added(filters, subscriptions, parsed_subscription, smtp)

    def on_subscription_deleted(self, subscription_deleted):
        """
        Subscriptions deleted. Searchs and delete a connection thread
        """
        st.logger.info('-----------------------')
        st.logger.info('Deleting subscription change...')
        thread = self.search_by_filter_id(subscription_deleted.filter_id)
        self.delete_connection(thread)

    def on_subscription_added(self, filters, subscriptions, subscription_added, notification_module):
        """
        Subscriptions added. Creates a new connection thread
        """
        st.logger.info('-----------------------')
        st.logger.info('New subscription change...')
        bus_filter = filters.get(subscription_added.filter_id)
        users = subscriptions.get_users_by_filter(bus_filter)
        st.logger.info('Notification to:  ' + str(users))
        self.create_connection(bus_filter, users, notification_module)

    def create_connection(self, bus_filter, users, notification_module):
        """
        Creates a thread with a new rabbitmq connection
        """
        bus_connection = BusConnectionHandler(bus_filter, users, notification_module)
        self.threads.append(bus_connection)
        bus_connection.start()

    def delete_connection(self, thread):
        """
        Search for a thread with the bus_filter to pause and delete it
        """
        st.logger.info('Stopping thread')
        thread.stop()
        self.threads.remove(thread)

    def search_by_filter_id(self, filter_id):
        """
        Searchs for a thread listening to a filter
        """
        for thread in self.threads:
            if thread.get_filter().id == filter_id:
                return thread

    def search_by_user(self, user):
        """
        Searchs for a thread listening to a list of users
        """
        for thread in self.threads:
            for user_thread in thread.get_users():
                if user_thread.email == user.email:
                    return thread

    def parse_filter(self, bus_filter):
        """
        Returns a BusFilter object from a realtime rethink object
        """
        if bus_filter['new_val']:
            parse_key = 'new_val'
        else:
            parse_key = 'old_val'

        return BusFilter(bus_filter[parse_key]['exchange'],
                         bus_filter[parse_key]['key'], bus_filter[parse_key]['id'])

    def parse_subscription(self, subscription):
        """
        Returns a Subscription object from a realtime rethink object
        """
        if subscription['new_val']:
            parse_key = 'new_val'
        else:
            parse_key = 'old_val'

        return Subscription(subscription[parse_key]['user_id'],
                            subscription[parse_key]['filter_id'])

