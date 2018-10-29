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
    def __init__(self, server, queue, exchange, keys, on_message_function ):
        self.server = server
        self.queue = queue
        self.exchange = exchange
        self.keys = keys
        self._is_interrupted = False
        self.on_message_function = on_message_function
        super(RabbitMqHandler, self).__init__()
    
    def stop(self):
        self._is_interrupted = True,
            
    def run(self):
        """
        Connect wit a rabbitMQ server
        """
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.server))
            self.channel = self.connection.channel()
            self.channel.exchange_declare(exchange=self.exchange,
                         exchange_type='direct')
            """
            NOTE: No queue name to let rabbit choouse a random name for us. 
            Is exclusive because it will be deleted when the connection closes
            """
            result = self.channel.queue_declare(exclusive=True)
            queue_name = result.method.queue

            for key in self.keys:
                self.channel.queue_bind(exchange=self.exchange,
                                        queue=queue_name,
                                        routing_key=key)

            st.logger.info('Waiting for bus messagges....')
            
            """
            NOTE: Instead of using basic consume, I use consume because basic cosume
            blocks the thread. With consume I can decide when the thread stops
            """
            for message in self.channel.consume(queue_name, inactivity_timeout=1):
                if self._is_interrupted:
                    break
                if not message:
                    continue
                method, properties, body = message
                self.on_message_function(method, properties, body)

        except Exception as e:
            st.logger.error(e)
            
    def on_message(self, method, properties, message):
        """"
        When a message is received
        """
        st.logger.info(' [x] Received from  %r:  |  %r' % (method.routing_key, message))
        # self.notification_module.send('dlopez@ets.es', 'Prueba', message)
