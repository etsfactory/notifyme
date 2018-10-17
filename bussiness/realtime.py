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
        to listen for a exchange and key in the bus
        """
        cursor = filters.get_realtime()
        smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
        
        for bus_filter in cursor:
            st.logger.info('-----------------------')
            st.logger.info('New change...')
            parsed_filter = BusFilter(bus_filter['new_val']['exchange'],
                                      bus_filter['new_val']['key'])
            st.logger.info('Watching for key:  ' + str(parsed_filter.__dict__))
            users = subscriptions.get_users_by_filter(parsed_filter)
            st.logger.info('Notification to:  ' + str(users))
            bus_connection = BusConnectionHandler(parsed_filter, users, smtp)
            self.threads.append(bus_connection)
            bus_connection.start()
            time.sleep(10)
            bus_connection.stop()
            
