"""
Main file program.
"""
# To run a sample database: sudo docker run --memory=4G --memory-swap=0 rethinkdb

import sys
import json
import os.path
import time

import errors
import settings as st
from threading import Thread

from connectors.rabbitmq import RabbitMqHandler
from connectors.smtp import SMTPHandler
from connectors.rethink import RethinkHandler
from connectors.data_streaming import DataStreaming

def rabbit():
    smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
    rabbit_handler = RabbitMqHandler(st.RABBITMQ_SERVER, 'hello', 'direct_logs', smtp)
    rabbit_handler.connect()

def bd_get(db):  
    print "Watching for changes..."
    cursor = db.get_data("users")
    for document in cursor:
        print document

def bd_set(db):
    while True:
        print "Inserting user...."
        db.insert_data("users", [
            { "name": "Diego", "email": "dlopez@ets.es" },
            { "name": "Diego", "email": "dlopez@ets.es" }
        ])
        time.sleep(5)

def main():
    # smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)

    db = RethinkHandler(st.DB_SERVER, st.DB_PORT, st.DB_NAME)
    watcher = DataStreaming(st.DB_SERVER, st.DB_PORT, st.DB_NAME)
    db.create_table("users")

    bd_set_thread = Thread(target=bd_set, args=(db,))
    bd_set_thread.start()

    time.sleep(1)
    bd_get_thread = Thread(target=bd_get, args=(watcher,))
    bd_get_thread.start()

    # rabbit_handler = RabbitMqHandler(st.RABBITMQ_SERVER, 'hello', 'direct_logs', smtp)
    # rabbit_handler.connect()
    # Captures not controlled exceptions
    sys.excepthook = errors.log_unhandled_exception

main()

