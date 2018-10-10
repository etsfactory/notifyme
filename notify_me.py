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

from bussiness.notification_types import NotificationTypeHandler
from bussiness.notification_types import NotificationType

from bussiness.subscription import SubscriptionHandler
from bussiness.subscription import Subscription

def rabbit():
    smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
    rabbit_handler = RabbitMqHandler(st.RABBITMQ_SERVER, 'hello', 'direct_logs', smtp)
    rabbit_handler.connect()

def bd_get_users(users):  
    time.sleep(4)
    print "Watching for user changes..."
    cursor = users.get_users_streaming()
    for document in cursor:
        print document

def bd_get_notifications(notifications):  
    
    time.sleep(4)
    while True:
        print notifications.get_notification_type()
        time.sleep(4)

def bd_get_subscriptions(subscriptions):  
    
    time.sleep(4)
    while True:
        print subscriptions.get_subscription()
        time.sleep(4)


def bd_set_user(users,):
    name = 0
    while True:
        print "Inserting user ...."
        users.insert_user(User("Diego", "dlopez@ets.es" + str(name)))
        name = name + 1
        time.sleep(4)

def bd_set_notification(notifications,):
    name = 0
    while True:
        print "Inserting notification ...."
        notifications.insert_notification_type(NotificationType("exchange" + str(name), "key"))
        name = name + 1
        time.sleep(4)
        
def bd_set_subscription(subscriptions,):
    name = 0
    while True:
        print "Inserting subscription ...."
        subscriptions.insert_subscription(Subscription("dlopez@ets.es1", "exchange" + str(name), "key"))
        name = name + 1
        time.sleep(4)
        
def main():
    # smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
    users = UsersHandler()
    notifications = NotificationTypeHandler()
    subscriptions = SubscriptionHandler()

    Thread(target=bd_set_user, args=(users,)).start()

    # Thread(target=bd_get_users, args=(users,)).start()
    
    Thread(target=bd_set_notification, args=(notifications,)).start()

    # Thread(target=bd_get_notifications, args=(notifications,)).start()

    Thread(target=bd_set_subscription, args=(subscriptions,)).start()

    Thread(target=bd_get_subscriptions, args=(subscriptions,)).start()

    # rabbit_handler = RabbitMqHandler(st.RABBITMQ_SERVER, 'hello', 'direct_logs', smtp)
    # rabbit_handler.connect()
    # Captures not controlled exceptions
    sys.excepthook = errors.log_unhandled_exception

main()

