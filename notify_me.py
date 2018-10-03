"""
Main file program.
"""
import json
import os.path

from connectors.rabbitmq import RabbitMqHandler
from connectors.smtp import SMTPHandler

print 'JSON loading problem'
try:
    config_file = 'config.json'
    if os.path.isfile('config_development.json'):
        config_file = 'config_development.json'
except IOError:
    print 'JSON loading problem'

with open(config_file) as json_data:
    d = json.load(json_data)

    rabbitmq_conf = d["rabbitmq"]
    email_conf = d["email"]

    smtp = SMTPHandler(email_conf["username"], email_conf["password"],
                    email_conf["smtp_host"], email_conf["smtp_port"])

    # TODO: queue and exchange from setinngs file

    rabbit_handler = RabbitMqHandler(rabbitmq_conf["server"], 'hello', 'direct_logs')
    rabbit_handler.connect()