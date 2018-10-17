"""
Bus connection handler
"""
from threading import Thread

import settings as st
from connectors.rabbitmq import RabbitMqHandler

class BusConnectionHandler(object): 
    """
    Bus connection class 
    """

    def __init__(self, bus_filter, users, notification_module):
        self.bus_filter = bus_filter
        self.users = users
        self.bus_thread = RabbitMqHandler(st.RABBITMQ_SERVER, 'notifyme', bus_filter, users, notification_module)

    def start(self):
        self.bus_thread.start()
    
    def stop(self):
        self.bus_thread.stop()

    def get_filter(self):
        return self.bus_filter