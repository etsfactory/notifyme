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
        self.filters = BusFiltersHandler()
        self.subscriptions = SubscriptionsHandler()
        self.smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
        Thread(target=self.realtime_filters).start()

    def realtime_filters(self):
        """
        Realtime filters. Creates a thread per new change
        to listen for a exchange and key in the bus.
        If a filter is removed, the bus connection stops listening and the thread is stopped
        If a filter is updated, the thread stops and creates and new thread
        """
        subs = self.subscriptions.get()
        for sub in subs:
            st.logger.info(sub)
            self.on_subscription_added(sub)

        cursor = self.subscriptions.get_realtime()

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
                self.on_subscription_added(parsed_subscription)

    def on_subscription_deleted(self, parsed_subscription):
        """
        Subscriptions deleted. Searchs and delete a connection thread
        """
        st.logger.info('-----------------------')
        st.logger.info('Deleting subscription change...')
        bus_filter = self.filters.get(parsed_subscription.filter_id)
        thread = self.search_thread(bus_filter.exchange)
        if thread: 
            self.delete_connection(thread)

    def on_subscription_added(self, parsed_subscription):
        """
        Subscriptions added. Creates a new connection thread
        """
        st.logger.info('-----------------------')
        st.logger.info('New subscription change...')
        
        self.on_subscription_deleted(parsed_subscription)   
        users_list = []
        keys = []
        exchange = self.filters.get(parsed_subscription.filter_id).exchange
        bus_filters = self.filters.get_by_exchange(exchange)
        for bus_filter in bus_filters:
            sub = self.subscriptions.get_by_filter(bus_filter)
            users = self.subscriptions.get_users_by_filter(bus_filter)
            if users:
                users_list.append(users)
            keys.append(bus_filter.key)
        st.logger.info('Notification to:  ' + str(users_list))
        st.logger.info('Notification to:  ' + str(keys))
        st.logger.info('Notification to:  ' + str(exchange))

        self.create_connection(exchange, keys, users_list, self.smtp)

    def create_connection(self, exchange, keys, users, notification_module):
        """
        Creates a thread with a new rabbitmq connection
        """
        bus_connection = BusConnectionHandler(exchange, keys, users, notification_module)
        self.threads.append(bus_connection)
        bus_connection.start()

    def delete_connection(self, thread):
        """
        Search for a thread with the bus_filter to pause and delete it
        """
        st.logger.info('Stopping thread')
        thread.stop()
        self.threads.remove(thread)

    def search_thread(self, exchange):
        """
        Searchs for a thread listening to a filter
        """
        for thread in self.threads:
            if thread.exchange == exchange:
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

