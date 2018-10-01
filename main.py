"""
Main file program.
"""

from handlers.rabbitmq import RabbitMqHandler
server = ''
while (server == ''):
    server = raw_input("Enter the url of the rabbitmq server: ")

handler = RabbitMqHandler()
handler.init()
