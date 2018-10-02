"""
Main file program.
"""
import json
import os.path

from notify_me.handlers.rabbitmq import RabbitMqHandler
from notify_me.handlers.smtp import SMTPHandler

try:
    config_file = 'config.json'
    if os.path.isfile('config_development.json'):
        config_file = 'config_development.json'

    with open(config_file) as json_data:
        d = json.load(json_data)
        email_conf = d["email"]
        smtp = SMTPHandler(email_conf["username"], email_conf["password"],
                           email_conf["smtp_host"], email_conf["smtp_port"])
        smtp.send_email('dlopez@ets.es', 'dlopez@ets.es', 'eeeeeeeeeee desde python')

except IOError:
    print 'JSON loading problem'

# handler = RabbitMqHandler(server)
# handler.init()
