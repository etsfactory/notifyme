"""
Bus connection handler
"""
import json
import settings as st

from connectors.rabbitmq import RabbitMqHandler
from bussiness.templates import Template
from bussiness.templates import TemplatesHandler

import utils.json_parser as json_parser

class BusConnectionHandler(object):
    """
    Bus connection class
    """
    def __init__(self, exchange, bus_filters, users, templates, notification_module):
        self.exchange = exchange
        self.bus_filters = bus_filters
        self.keys = []
        self.users = users
        self.templates = templates
        self.initialize_keys()
        self.bus_thread = RabbitMqHandler(st.RABBITMQ_SERVER, 'notifyme', exchange, self.keys, users, notification_module, self.on_message)

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

    def initialize_keys(self):
        for bus_filter in self.bus_filters:
            print(str(bus_filter.__dict__))
            self.keys.append(bus_filter.key)

    def get_exchange(self):
        """
        Return the exchange that it's listening the thread
        """
        return self.exchange
    
    def is_watching_exchange(self, exchange):
        return exchange == self.exchange
    
    def on_message(self, method, properties, message):
        """"
        When a message is received
        """
        response = json_parser.from_json(message)
        for user in self.users:
            template = self.templates[self.users.index(user)]
            st.logger.info(' [x] Received from  %r:  |  %r' % 
            (method.exchange, template.parse(response)))
            st.logger.info('Notification to: %r' % (user.email))
        
        # self.notification_module.send('dlopez@ets.es', 'Prueba', message)
