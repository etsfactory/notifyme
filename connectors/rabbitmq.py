""""
RabbitMQ handler
"""
import pika
import threading
import settings as st


class RabbitMqHandler(threading.Thread):
    """
    Class to manage connection with a rabbitMQ server
    """
    def __init__(self, server, queue, bus_filter, users, notification_module ):
        self.server = server
        self.queue = queue
        self.bus_filter = bus_filter
        self.notification_module = notification_module
        self.connect()
        super().__init__()
    
    def stop(self):
        self.channel.stop_consuming()
        if self.channel.is_open:
                self.channel.stop_consuming()
                self.connection.close()
            
    def connect(self):
        """
        Connect wit a rabbitMQ server
        """
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.server))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=self.bus_filter.exchange,
                         exchange_type='direct')
            """
            NOTE: No queue name to let rabbit choouse a random name for us. 
            Is exclusive because it will be deleted when the connection closes
            """
            result = self.channel.queue_declare(exclusive=True)
            queue_name = result.method.queue

            self.channel.queue_bind(exchange=self.bus_filter.exchange,
                                    queue=queue_name,
                                    routing_key=self.bus_filter.key)

            st.logger.info('Waiting for bus messagges....')
            
            self.channel.basic_consume(self.on_message,
                                    queue=queue_name)

        except Exception as e:
            st.logger.error(e)
            
    def run(self):
        """
        Start listening for a queue
        """
        st.logger.info('Starting listening for messagges....')
        try:
            self.channel.start_consuming()
        except Exception as e:
            st.logger.error(e)

    def on_message(self, ch, method, properties, message):
        """"
        When a message is received
        """
        st.logger.info(' [x] Received from  %r:  |  %r' % (method.routing_key, message))
        # self.notification_module.send('dlopez@ets.es', 'Prueba', message)
