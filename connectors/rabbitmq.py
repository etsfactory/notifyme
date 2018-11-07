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

class RabbitMqHandler(threading.Thread):
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
        super(RabbitMqHandler, self).__init__()
    
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
                self.channel.queue_bind(exchange=sub['exchange'],
                                        queue=self.queue,
                                        routing_key=sub['key'])
               
            st.logger.info('Waiting for bus messagges....')
            retries = 0
            self.listen(self.queue)

        except (ConnectionClosed, ConnectionErrorException) as e:
                """
                Only publishes the first error to the error queue
                """
                if retries == self.retries_to_error:
                    exception = {
                        'error': e,
                        'trace': traceback.format_exc()
                    }
                    if (self.error_exchange):
                        self.send_message(self.error_exchange, exception)
                try:
                    self.channel.close()
                except Exception:
                    pass
        except Exception as e:
            exception = {
                'error': e,
                'trace': traceback.format_exc()
            }
            if (self.error_exchange):
                self.send_message(self.error_exchange, exception)
        finally:
            retries += 1
            time.sleep(self.retry_wait_time)
    
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
    
    def send_message(self, exchange, message, routing_key=''):
        self.channel.exchange_declare(exchange=exchange,
                            exchange_type='direct')

        self.channel.basic_publish(exchange=exchange,
                      routing_key=routing_key,
                      body=message,)
