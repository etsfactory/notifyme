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

from bussiness.subscriptions import SubscriptionsHandler
from bussiness.subscriptions import Subscription

from bussiness.realtime import Realtime
from api.api import ApiHandler
        
def initiliceTestData():

    users = UsersHandler()
    filters = BusFiltersHandler()
    subscriptions = SubscriptionsHandler()
    
    users.insert(User("Bruno", "bcontreras@ets.es"))
    users.insert(User("Diego", "dlopez@ets.es"))
    
    filters.insert(BusFilter("logs", "important"))
    filters.insert(BusFilter("logs", "info"))

def main():
    # smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)
    
    st.logger.info('Starting service')

    # initiliceTestData()

    Realtime()

    api = ApiHandler()
    api.start()

    # Captures not controlled exceptions
    sys.excepthook = errors.log_unhandled_exception

main()
