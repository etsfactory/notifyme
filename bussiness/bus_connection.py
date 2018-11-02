"""
Bus connection handler
"""
import json
import settings as st

from connectors.rabbitmq import RabbitMqHandler
from bussiness.templates import Template
from bussiness.templates import TemplatesHandler
from connectors.smtp import SMTPHandler

from bussiness.users import UsersHandler
from bussiness.users import User
from bussiness.bus_filters import BusFilter
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionsHandler
from bussiness.subscriptions import Subscription
from bussiness.templates import Template
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
        self.initialize()

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

    def initialize(self):
        """
        Create keys to listen
        """
        self.bus_thread = RabbitMqHandler(self.on_message, st.RABBITMQ_SERVER,
                                          st.RABBITMQ_USER, st.RABBITMQ_PASSWORD, 'notifyme', self.subscriptions, 'error')

    def is_listening_subscription(self, subscription):
        """
        Check if the thread is listening to a subscription bus_filter
        """
        for sub in self.subscriptions:
            exchange1 = self.filters_handler.get(sub['filter_id']).exchange
            exchange2 = self.filters_handler.get(
                subscription.filter_id).exchange
            if exchange1 == exchange2:
                return True
        return False

    def on_message(self, method, properties, message):
        """"
        When a message is received
        """
        response = json_parser.from_json(message)
        bus_filter = self.filters_handler.get_by_exchange_key(
            method.exchange, method.routing_key)

        for sub in self.subscriptions_handler.get_by_filter(bus_filter):
            user = self.users_handler.get(sub.user_id)
            template = self.templates_handler.get(sub.template_id)

            st.logger.info(' [x] Received from  %r:  |  %r' %
                           (method.exchange, self.templates_handler.parse(template.text, response)))
            st.logger.info('Notification to: %r' % (user.email))
          # self.smtp.send(user.email, self.templates_handler.parse(template.subject, response), self.templates_handler.parse(template.text, response))
