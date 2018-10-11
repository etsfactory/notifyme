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

from bussiness.bus_filters import BusFiltersHandler
from bussiness.bus_filters import BusFilter

from bussiness.subscriptions import SubscriptionHandler
from bussiness.subscriptions import Subscription

def rabbit(exchange, key):
    smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
    rabbit_handler = RabbitMqHandler(st.RABBITMQ_SERVER, 'hello', exchange, smtp, [key] )
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
    cursor = subscriptions.get_subscription_streaming()
    for document in cursor:
         print document
         # Thread(target=rabbit, args=(document['new_val']['exchange'], document['new_val']['key'],)).start()

def bd_set_user(users,):
    name = 0
    while True:
        print "Inserting user ...."
        users.insert_user(User("Diego", "dlopez@ets.es" + str(name)))
        name = name + 1
        time.sleep(4)

def bd_set_notification(filters,):
    name = 0
    while True:
        print "Inserting filter ...."
        filters.insert_bus_filter(BusFilter("exchange", "key"))
        name = name + 1
        time.sleep(4)
        
def bd_set_subscription(subscriptions,):
    name = 0
    while True:
        print "Inserting subscription ...."
        # subscriptions.insert_subscription(Subscription("dlopez@ets.es1", "exchange", "key"))
        name = name + 1
        time.sleep(4)
        
def main():
    # smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
    users = UsersHandler()
    filters = BusFiltersHandler()
    subscriptions = SubscriptionHandler()
    users.insert(User("Bruno", "bcontreras@ets.es"))
    users.insert(User("Diego", "dlopez@ets.es"))
    users.edit(User("Diego Lopez", "dlopez@ets.es"))
    filters.insert(BusFilter("logs", "important"))
    print users.get_by_email("dlopez@ets.es").name
    # for filter in filters.get_bus_filters():
    #    print filter
    subscriptions.insert(Subscription("dlopez@ets.es", ['logs', 'important']))
    subscriptions.insert(Subscription("bcontreras@ets.es", ['logs', 'important']))

    print '------------'
    for user in subscriptions.get_users_by_filter(BusFilter('logs', 'important')):
        print str(user.__dict__)
    
    for bus_filter in subscriptions.get_filters_by_user(User("Bruno", "bcontreras@ets.es")):
        print str(bus_filter.__dict__)
    
    # users.insert_user(st.USERS)
    # print parser.to_json(User("Diego", "dlopez@ets.es"))
    time.sleep(1)

    # Thread(target=bd_set_user, args=(users,)).start()

    # Thread(target=bd_get_users, args=(users,)).start()
    
    # Thread(target=bd_set_notification, args=(filters,)).start()

    # Thread(target=bd_get_notifications, args=(notifications,)).start()
    #time.sleep(4)

    # Thread(target=bd_set_subscription, args=(subscriptions,)).start()

    # Thread(target=bd_get_subscriptions, args=(subscriptions,)).start()

    # rabbit_handler = RabbitMqHandler(st.RABBITMQ_SERVER, 'hello', 'direct_logs', smtp)
    # rabbit_handler.connect()
    # Captures not controlled exceptions
    sys.excepthook = errors.log_unhandled_exception

main()

