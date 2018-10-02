"""
Main file program.
"""
from handlers.rabbitmq import RabbitMqHandler
from handlers.smtp import SMTPHandler
import json
import os.path

try:
   config_file = 'config.json'
    if os.path.isfile('config_development.json'):
        config_file = 'config_development.json'

    with open(config_file) as json_data:
        d = json.load(json_data)
        smtp = SMTPHandler(d["email"]["username"],d["email"]["password"])
        smtp.send_email('dlopez@ets.es','dlopez@ets.es', 'eeeeeeeeeee desde python')
except:
    print 'JSON loading problem'
# handler = RabbitMqHandler(server)
# handler.init()
