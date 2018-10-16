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
    def __init__(self, server, queue, bus_filter, users, smtp ):
        self.server = server
        self.queue = queue
        self.bus_filter = bus_filter
        self.smtp = smtp
        self.connect()
        super().__init__()

    def connect(self):
        """
        Connect wit a rabbitMQ server
        """
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(self.server))
            self.channel = connection.channel()
            result = self.channel.queue_declare(exclusive=True)
            queue_name = result.method.queue

            self.channel.queue_bind(exchange=self.bus_filter.exchange,
                   queue=queue_name)

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
            st.logger.error('Error')

    def on_message(self, ch, method, properties, message):
        """"
        When a message is received
        """
        st.logger.info(' [x] Received %r' % message)
        # self.smtp.send_email('dlopez@ets.es', 'Prueba', message)
