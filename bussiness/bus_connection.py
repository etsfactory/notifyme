"""
Bus connection handler
"""
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

    def get_filter(self):
        """
        Return the bus filter that it's listening the thread
        """
        return self.bus_filter
