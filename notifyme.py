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

from bussiness.realtime import Realtime
from api.api import ApiHandler

def main():

    st.logger.info('Starting notifyme...')

    Realtime()

    api = ApiHandler()
    api.start()

    # Captures not controlled exceptions
    sys.excepthook = errors.log_unhandled_exception


main()
