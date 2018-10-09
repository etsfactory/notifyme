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
from bussiness.users import UsersHandler
from bussiness.users import User

def rabbit():
    smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
    rabbit_handler = RabbitMqHandler(st.RABBITMQ_SERVER, 'hello', 'direct_logs', smtp)
    rabbit_handler.connect()

def bd_get(users):  
    
    print "Watching for changes..."
    cursor = users.get_users_streaming()
    for document in cursor:
        print document

def bd_set(users):
    name = 0    
    while True:
        print "Inserting user...."
        users.insert_user(User("Diego", "dlopez@ets.es"))
        time.sleep(4)
        print "Updating user...."
        users.edit_user(User("Diego Lopez", "dlopez@ets.es"))
        time.sleep(4)
        name = name + 1

def main():
    # smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
    users = UsersHandler()
    # users.insert_user(st.USERS)
    
    bd_get_thread = Thread(target=bd_get, args=(users,))
    bd_get_thread.start()

    time.sleep(1)
    bd_set_thread = Thread(target=bd_set, args=(users,))
    bd_set_thread.start()

    # rabbit_handler = RabbitMqHandler(st.RABBITMQ_SERVER, 'hello', 'direct_logs', smtp)
    # rabbit_handler.connect()
    # Captures not controlled exceptions
    sys.excepthook = errors.log_unhandled_exception

main()

