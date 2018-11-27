"""
Bus connection handler
"""
import json
import queue
import settings as st
from jinja2 import Template

from raccoon import Consumer
import errors

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

    def start(self):
        """
        Starts the thread
        """
        if (len(self.subscriptions) > 0):
            error = queue.Queue()
            self.bus_thread = Consumer(
                self.on_message,
                st.RABBITMQ_SERVER,
                st.RABBITMQ_USER,
                st.RABBITMQ_PASSWORD,
                self.subscriptions,
                st.RABBITMQ_QUEUE,
                error)

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
        if bus_filter:
            for sub in self.subscriptions_handler.get_by_filter(bus_filter):
                user = self.users_handler.get(sub['user_id'])
                template = self.templates_handler.get(sub['template_id'])
                st.logger.info('Notification to: %r' % (user['email']))
                
                subject_t = Template(template.get('subject'))
                text_t = Template(template.get('text'))

                subject = subject_t.render(message)
                text = text_t.render(message)

                self.smtp.send(user['email'], subject, text)

    def set_subscriptions(self, subscriptions):
        self.subscriptions = subscriptions
    
    def unbind(self, exchange, key):
        self.bus_thread.unbind_queue(exchange, key)
