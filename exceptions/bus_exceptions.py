import settings as st
import errors as e
import traceback

class BusException(Exception):
    def __init__(self, msg, original_exception):
        super(BusException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception
        e.process_exception(self.original_exception, msg)
    
class ConnectionErrorException(BusException):
    """Basic exception for errors raised by inserting into the database"""
    def __init__(self, msg=None):
        self.name = 'Connection error'
        if msg is None:
            msg = "The bus connection is closed"
        super(ConnectionErrorException, self).__init__(msg)

