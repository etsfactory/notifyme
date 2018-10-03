""""
RabbitMQ handler
"""
import pika

class RabbitMqHandler(object):
    """
    Class to manage connection with a rabbitMQ server
    """
    keys = []

    def __init__(self, server, email_handler):
        print server
        self.server = server
        self.keys.append('black')
        self.email_handler = email_handler

    def connect(self):
        """
        Connect wit a raabbitMQ server
        """
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.server))
        self.channel = connection.channel()

        # It ensures that the queue exists
        self.channel.queue_declare(queue='hello')
        self.consume('hello')

    def consume(self, queue):
        """
        Start listening for a queue with a list of keys
        """
        for key in self.keys:
            print "Watching key %s" % key
            self.channel.queue_bind(exchange='direct_logs', queue=queue, routing_key=key)

        self.channel.basic_consume(self.on_message,
                                   queue=queue)

        print ' [*] Waiting for messages. To exit press CTRL+C'
        self.channel.start_consuming()

    def on_message(self, ch, method, properties, message):
        """"
        When a message is received
        """
        print ' [x] Received %r' % message
        self.email_handler.send_email('dlopez@ets.es', 'Pruebas desde python con rabbitMQ', message)
