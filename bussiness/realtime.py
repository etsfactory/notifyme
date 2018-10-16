"""
Realtime module
"""

from threading import Thread

import settings as st
from bussiness.bus_filters import BusFilter
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionHandler
from connectors.rabbitmq import RabbitMqHandler
from connectors.smtp import SMTPHandler

class Realtime(object):
    """
    Realtime class
    """
    def __init__(self):
        filters = BusFiltersHandler()
        subscriptions = SubscriptionHandler()
        Thread(target=self.realtime_filters, args=(filters, subscriptions)).start()

    def realtime_filters(self, filters, subscriptions):
        """
        Realtime filters. Creates a thread per new change
        to listen for a exchange and key in the bus
        """
        cursor = filters.get_realtime()
        for bus_filter in cursor:
            st.logger.info('-----------------------')
            st.logger.info('New change...')
            parsed_filter = BusFilter(bus_filter['new_val']['exchange'],
                                      bus_filter['new_val']['key'])
            st.logger.info('Watching for key:  ' + str(parsed_filter.__dict__))
            users = subscriptions.get_users_by_filter(parsed_filter)
            st.logger.info('Notification to:  ' + str(users))
            rmq_tread = Thread(target=self.new_connection, args=(parsed_filter, users))
            rmq_tread.start()

    def new_connection(self, bus_filter, users):
        """
        Creates a new connection with bus
        """
        st.logger.info('Starting new thread...')
        smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
        rabbit_handler = RabbitMqHandler(st.RABBITMQ_SERVER, 'notifyme', bus_filter, users, smtp)
        rabbit_handler.run()
