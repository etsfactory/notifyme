import pika

class RabbitMqHandler:
    server = 'localhost'
    channel = ''
    keys = []

    def __init__(self, server):
        self.server = server
        self.keys.append('black')

    def consume(self, queue):
        for key in self.keys:
            print "Watching key %s" % key
            bind_promise = self.channel.queue_bind(exchange='direct_logs', queue=queue, routing_key=key)
            consumer.wait(bind_promise)

        self.channel.basic_consume(self.on_message,
                                queue=queue)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def init(self):

        connection = pika.BlockingConnection(pika.ConnectionParameters(self.server))
        self.channel = connection.channel()

        # It ensures that the queue exists
        self.channel.queue_declare(queue='hello')
        self.consume('hello')

    # This funcions is executed when a message is received
    def on_message(ch, method, properties, body):
        print(" [x] Received %r" % body)

        # ACK, if the worker dies, the message will be redelivered
        ch.basic_ack(delivery_tag = method.delivery_tag)

