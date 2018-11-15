"""
Bus connection handler
"""
import json
import queue
import settings as st

from connectors.rabbitmq import RabbitMqConsumer
from connectors.smtp import SMTPHandler

from bussiness.users import UsersHandler
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionsHandler
from bussiness.templates import TemplatesHandler

import utils.json_parser as json_parser

class BusConnectionHandler(object):
    """
    Bus connection class
    """

    def __init__(self, subscriptions):
        self.subscriptions = subscriptions
        self.users = []
        self.filters_handler = BusFiltersHandler()
        self.subscriptions_handler = SubscriptionsHandler()
        self.users_handler = UsersHandler()
        self.templates_handler = TemplatesHandler()
        self.smtp = SMTPHandler(
            st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
        error = queue.Queue()
        self.bus_thread = RabbitMqConsumer(self.on_message, st.RABBITMQ_SERVER,
                            st.RABBITMQ_USER, st.RABBITMQ_PASSWORD, self.subscriptions,
                            st.RABBITMQ_QUEUE,  error, exchange_type='direct')

    def start(self):
        """
        Starts the thread
        """
        self.bus_thread.start()

    def stop(self):
        """
        Stops the thread
        """
        self.bus_thread.stop()
        self.bus_thread.join()

    def is_listening_subscription(self, subscription):
        """
        Check if the thread is listening to a subscription bus_filter
        """
        for sub in self.subscriptions:
            exchange1 = self.filters_handler.get(sub['filter_id'])['exchange']
            exchange2 = self.filters_handler.get(
                subscription['filter_id'])['exchange']
            if exchange1 == exchange2:
                return True
        return False

    def on_message(self, method, properties, message):
        """"
        When a message is received
        """
        bus_filter = self.filters_handler.get_by_exchange_key(
            method.exchange, method.routing_key)
        for sub in self.subscriptions_handler.get_by_filter(bus_filter):
            user = self.users_handler.get(sub['user_id'])
            template = self.templates_handler.get(sub['template_id'])

            st.logger.info('Notification to: %r' % (user['email']))
            self.smtp.send(user['email'], self.templates_handler.parse(template['subject'], message), self.templates_handler.parse(template['text'], message))
