"""
Main file program.
"""
import sys
import json
import os.path

import errors
import settings as st

from connectors.rabbitmq import RabbitMqHandler
from connectors.smtp import SMTPHandler
from connectors.rethink import RethinkHandler

def main():

    smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
    db = RethinkHandler()
    
    # rabbit_handler = RabbitMqHandler(st.RABBITMQ_SERVER, 'hello', 'direct_logs', smtp)
    # rabbit_handler.connect()

    # Captures not controlled exceptions
    sys.excepthook = errors.log_unhandled_exception

main()
