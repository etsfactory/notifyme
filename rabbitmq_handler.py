import pika

class RabbitMqHandler:
    url = 'localhost'
    channel = ''

    def consume(self, queue):
        self.channel.basic_consume(self.on_message,
                        queue='hello',
                        no_ack=True)

        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming().getLogger(queue)

    def init(self):

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        self.channel = connection.channel()

        # It ensures that the queue exists
        self.channel.queue_declare(queue='hello')
        self.consume('test1')

    # This funcions is executed when a message is received
    def on_message(ch, method, properties, body):
        print(" [x] Received %r" % body)

