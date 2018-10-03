""""
RabbitMQ handler
"""
import pika

class RabbitMqHandler(object):
    """
    Class to manage connection with a rabbitMQ server
    """
    def __init__(self, server, queue, exchange, smtp=None, keys=[]):
        self.server = server
        self.keys = keys
        self.queue = queue
        self.exchange = exchange
        self.smtp = smtp

    def connect(self):
        """
        Connect wit a raabbitMQ server
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.server))
        self.channel = connection.channel()

        # It ensures that the queue exists
        self.channel.queue_declare(queue=self.queue)
        self.consume(self.queue)

    def consume(self, queue):
        """
        Start listening for a queue with a list of keys
        """
        for key in self.keys:
            print "Watching key %s" % key
            self.channel.queue_bind(exchange=self.exchange, queue=queue, routing_key=key)
        
        if len(self.keys) == 0: 
            self.channel.queue_bind(exchange=self.exchange, queue=queue)

        self.channel.basic_consume(self.on_message,
                                   queue=queue)

        print ' [*] Waiting for messages. To exit press CTRL+C'
        self.channel.start_consuming()

    def on_message(self, ch, method, properties, message):
        """"
        When a message is received
        """
        print ' [x] Received %r' % message
        self.smtp.send_email('dlopez@ets.es', 'Prueba para release 0.1.0', message)
