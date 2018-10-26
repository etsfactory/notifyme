"""
Bus connection handler
"""
import settings as st
from connectors.rabbitmq import RabbitMqHandler

class BusConnectionHandler(object):
    """
    Bus connection class
    """
    def __init__(self, exchange, keys, users, notification_module):
        self.exchange = exchange
        self.keys = keys
        self.users = users
        self.bus_thread = RabbitMqHandler(st.RABBITMQ_SERVER, 'notifyme', exchange, keys, users, notification_module)

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