"""
Realtime module
"""
import time
from threading import Thread

import settings as st
from bussiness.bus_filters import BusFilter
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionHandler
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
        subscriptions = SubscriptionHandler()
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
                '''
                When a subscription is deleted
                '''
                st.logger.info('-----------------------')
                st.logger.info('Deleting subscription change...')
                thread = self.search_by_filter(parsed_subscription.exchange_key)
                self.delete_connection(thread)
            if subscription['new_val']:
                '''
                When a subscription is added or edited
                '''
                st.logger.info('-----------------------')
                st.logger.info('New filter change...')
                bus_filter = filters.get_by_exchange_key(parsed_subscription.exchange_key)
                users = subscriptions.get_users_by_filter(bus_filter)
                st.logger.info('Notification to:  ' + str(users))
                self.create_connection(bus_filter, users, smtp)
                

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
    
    def search_by_filter(self, filter_key):
        for thread in self.threads:
            if thread.get_filter().exchange_key == filter_key:
                return thread
    

    def search_by_user(self, user):
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
                         bus_filter[parse_key]['key'])
        
    def parse_subscription(self, subscription):
       
        if subscription['new_val']:
            parse_key = 'new_val'
        else: 
            parse_key = 'old_val'

        return Subscription(subscription[parse_key]['email'],
                        subscription[parse_key]['exchange_key'])