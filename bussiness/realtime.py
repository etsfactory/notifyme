"""
Realtime module
"""
import time
from threading import Thread

import settings as st
from bussiness.bus_filters import BusFilter
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionHandler
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
        cursor = filters.get_realtime()
        smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
        
        for bus_filter in cursor:
            st.logger.info(bus_filter)
            parsed_filter = self.parse_filter(bus_filter)
            if bus_filter['old_val']:
                '''
                When a filter is deleted
                '''
                st.logger.info('-----------------------')
                st.logger.info('Deleting filter change...')
                st.logger.info('Watching for key:  ' + str(parsed_filter.__dict__))
                self.delete_connection(parsed_filter)
            if bus_filter['new_val']:
                '''
                When a filter is added or edited
                '''
                st.logger.info('-----------------------')
                st.logger.info('New filter change...')
                st.logger.info('Watching for key:  ' + str(parsed_filter.__dict__))
                users = subscriptions.get_users_by_filter(parsed_filter)
                st.logger.info('Notification to:  ' + str(users))
                self.create_connection(parsed_filter, users, smtp)
                
            
    def create_connection(self, bus_filter, users, notification_module):
        """
        Creates a thread with a new rabbitmq connection
        """
        bus_connection = BusConnectionHandler(bus_filter, users, notification_module)
        self.threads.append(bus_connection)
        bus_connection.start()

    def delete_connection(self, bus_filter):
        """
        Search for a thread with the bus_filter to pause and delete it
        """
        for thread in self.threads:
            if thread.get_filter().exchange_key == bus_filter.exchange_key:
                st.logger.info('Stopping thread')
                thread.stop()

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
    
    