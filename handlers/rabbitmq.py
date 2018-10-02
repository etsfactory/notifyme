import pika

class RabbitMqHandler:
    server = 'localhost'
    channel = ''
    queue = 'hello'
    keys = []

    def __init__(self, server):
        self.server = server
        self.keys.append('black')

    def init(self):

        connection = pika.BlockingConnection(pika.ConnectionParameters(self.server))
        self.channel = connection.channel()

        # It ensures that the queue exists
        self.channel.queue_declare(queue=self.queue)
        self.consume(self.queue)

    def consume(self, queue_name):
        for key in self.keys:
            print "Watching key %s" % key
            self.channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=key)

        self.channel.basic_consume(self.on_message,
                              queue=queue_name,
                              no_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    # This funcions is executed when a message is received
    def on_message(ch, method, properties, body, message):
        print(" [x] Received %r" % message)

        # ACK, if the worker dies, the message will be redelivered
        # ch.basic_ack(delivery_tag = method.delivery_tag)

