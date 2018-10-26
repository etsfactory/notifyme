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
    def __init__(self, exchange, keys, users, templates, notification_module):
        self.exchange = exchange
        self.keys = keys
        self.users = users
        self.templates = templates
        self.bus_thread = RabbitMqHandler(st.RABBITMQ_SERVER, 'notifyme', exchange, keys, users, notification_module, self.on_message)

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

    def get_keys(self):
        """
        Return the keys that it's listening the thread
        """
        return self.keys

    def get_exchange(self):
        """
        Return the exchange that it's listening the thread
        """
        return self.exchange
    
    def is_watching_key(self, key):
        return key in self.keys
    
    def add_key(self, key):
        return self.keys.append(key)

    def remove_key(self, key):
        self.keys.remove(key)

    def on_message(self, method, properties, message):
        """"
        When a message is received
        """
        response = json_parser.from_json(message)
        for template in self.templates:
            st.logger.info(' [x] Received from  %r:  |  %r' % 
            (method.routing_key, template.parse(response)))
        
        
        # self.notification_module.send('dlopez@ets.es', 'Prueba', message)
