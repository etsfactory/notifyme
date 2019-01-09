"""
Main file program.
"""
# To run a sample database:
# sudo docker run --memory=4G --memory-swap=0 rethinkdb

import sys
import errors
import settings as st

from bussiness.realtime import Realtime
from api.v1.api import ApiHandler


def main():
    """
    Main program file
    """

    st.logger.info('Starting notifyme...')

    Realtime()

    api = ApiHandler()
    api.start()

    # Captures not controlled exceptions
    sys.excepthook = errors.log_unhandled_exception


main()