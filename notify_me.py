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

from bussiness.realtime import Realtime
        
def main():
    # smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
    users = UsersHandler()
    filters = BusFiltersHandler()
    subscriptions = SubscriptionHandler()
    
    users.insert(User("Bruno", "bcontreras@ets.es"))
    users.insert(User("Diego", "dlopez@ets.es"))
    users.edit(User("Diego Lopez", "dlopez@ets.es"))
    
    filters.insert(BusFilter("logs2", "important"))
    
    # for filter in filters.get_bus_filters():
    #    print filter
   
    subscriptions.insert(Subscription("dlopez@ets.es", ['logs', 'important']))
    subscriptions.insert(Subscription("dlopez@ets.es", ['logs2', 'important']))
    subscriptions.insert(Subscription("bcontreras@ets.es", ['logs3', 'important']))

    st.logger.info('Starting service')

    Realtime()

    time.sleep(5)
    filters.insert(BusFilter("logs", "important"))
    
    time.sleep(5)
    filters.insert(BusFilter("logs", "info"))
    
    time.sleep(5)
    filters.delete(BusFilter("logs", "info"))

    # Captures not controlled exceptions
    sys.excepthook = errors.log_unhandled_exception

main()
