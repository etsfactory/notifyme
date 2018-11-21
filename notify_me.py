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
    filters.insert({"exchange": "notifications", "key": "important", "exchange_type": "direct"})


def main():

    st.logger.info('Starting notifyme...')

    if (st.REFRESH_DATABASE):
        initiliceTestData()

    Realtime()

    api = ApiHandler()
    api.start()

    # Captures not controlled exceptions
    sys.excepthook = errors.log_unhandled_exception


main()
