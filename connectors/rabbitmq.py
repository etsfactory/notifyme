""""
RabbitMQ handler
"""
import pika
import threading
import traceback
import time

import settings as st

from pika.exceptions import ConnectionClosed
from exceptions.bus_exceptions import ConnectionErrorException
from utils.json_parser import to_json

class RabbitMqConsumer(threading.Thread):
    """
    Class to manage connection with a rabbitMQ server
    """
    def __init__(self, on_message_function, server, user, password, queue, exchange_keys, error_exchange, exchange_type='direct', retries_to_error=3, retry_wait_time=1, heartbeat=None ):
        self.on_message_function = on_message_function
        self.server = server
        self.user = user
        self.password = password
        self.queue = queue
        self.exchange_keys = exchange_keys
        self.error_exchange = error_exchange
        self.exchange_type = exchange_type
        self.retries_to_error = retries_to_error
        self.retry_wait_time = retry_wait_time
        self.heartbeat  = heartbeat
        self._is_interrupted = False
        self.rabbitmq_publisher = RabbitMQPublisher(self.server, self.user, self.password, self.error_exchange)

        super(RabbitMqConsumer, self).__init__()
    
    def stop(self):
        self._is_interrupted = True,
    
    def set_exchange_keys(self, exchange_keys):
        self.exchange_keys = exchange_keys
            
    def run(self):
        """
        Connect wit a rabbitMQ server
        """
        retries = 0
        try:
            if self.user and self.password:
                credentials = pika.PlainCredentials(self.user, self.password)
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(self.server, credentials=credentials))
            else:
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(self.server))

            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)
         
            for sub in self.exchange_keys:
                self.channel.exchange_declare(exchange=sub['exchange'],
                            exchange_type=self.exchange_type)

            for sub in self.exchange_keys:
                if sub['key'] != '':
                    self.channel.queue_bind(exchange=sub['exchange'],
                                            queue=self.queue,
                                            routing_key=sub['key'])
                else:
                    self.channel.queue_bind(exchange=sub['exchange'],
                                            queue=self.queue)
               
            st.logger.info('Waiting for bus messagges....')
            retries = 0
            self.listen(self.queue)

        except (ConnectionClosed, ConnectionErrorException):
                try:
                    self.channel.close()
                except Exception:
                    pass
        except Exception:
            pass
        
    def listen(self, queue_name):
        """
        Instead of using basic consume, I use consume because basic cosume
        blocks the thread. With consume I can decide when the thread stops
        """
        for message in self.channel.consume(queue_name, inactivity_timeout=1):
            if self._is_interrupted:
                break
            if not message:
                continue
            method, properties, body = message
            
            self.channel.basic_ack(delivery_tag=method.delivery_tag)
            self.on_message_function(method, properties, body)
    
class RabbitMQPublisher():

    def __init__(self, server, user, password, exchange, exchange_type='direct', retry_wait_time=1, max_retries=1,):
        self.server = server
        self.user = user
        self.password = password
        self.exchange = exchange
        self.exchange_type = exchange_type
        self.retry_wait_time = retry_wait_time
        self.max_retries  = max_retries
        
    def __enter__(self):
        try:
            tries = 0
            finished = False
            connection_out = None
            while not finished:
                try:
                    if self.user and self.password:
                        credentials = pika.PlainCredentials(self.user, self.password)
                        connection_out = pika.BlockingConnection(pika.ConnectionParameters(self.server, credentials=credentials))
                    else:
                        connection_out = pika.BlockingConnection(pika.ConnectionParameters(self.server))
                    finished = True
                except ConnectionClosed as e:
                    print('Tries: %s, maxTries: %s' % (tries, self.max_retries))
                    if tries > self.max_retries:
                        raise e
                    time.sleep(10)
                    tries += 1
            self.channel = connection_out.channel()
            self.channel.exchange_declare(exchange=self.exchange, exchange_type=self.exchange_type)
        except Exception as e:
            print(e)
        return self

    def __exit__(self, type, value, traceback):
        self.channel.close()

    def send_message(self, message, routing_key=''):
        if isinstance(message, dict):
            message = to_json(message)
        self.channel.basic_publish(exchange=self.exchange,
                    routing_key=routing_key,
                    body=message)

        
                    
