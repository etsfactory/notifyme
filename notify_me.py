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
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionsHandler

from bussiness.realtime import Realtime
from api.api import ApiHandler


def initiliceTestData():

    users = UsersHandler()
    filters = BusFiltersHandler()
    subscriptions = SubscriptionsHandler()

    users.insert({"name": "Diego", "email": "dlopez@ets.es"})

    filters.insert({"exchange": "notifications", "key": "important"})


def main():
    # smtp = SMTPHandler(st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)

    st.logger.info('Starting service')

    if (st.REFRESH_DATABASE):
        initiliceTestData()

    Realtime()

    api = ApiHandler()
    api.start()

    # Captures not controlled exceptions
    sys.excepthook = errors.log_unhandled_exception


main()
