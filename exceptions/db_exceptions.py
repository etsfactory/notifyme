import settings as st
import traceback
import errors as e

class DBException(Exception):
    def __init__(self, name, msg):
        super(DBException, self).__init__(msg)
        e.process_exception('a', name, msg)
    
class WriteError(DBException):
    """Basic exception for errors raised by inserting into the database"""
    def __init__(self, msg=None):
        self.name = 'DB Write error'
        if msg is None:
            msg = "An error occured inserting into database"
        super(WriteError, self).__init__(self.name, msg)

class ReadError(DBException):
    """Basic exception for errors raised by reading from the database"""
    def __init__(self, msg=None):
        self.name = 'DB read error'
        if msg is None:
            msg = "An error occured reading from the database"
        super(ReadError, self).__init__(self.name, msg)

class ConnectionLost(DBException):
    """ If the connection is lost"""
    def __init__(self, msg=None):
        self.name = 'DB connection error'
        if msg is None:
            msg = "Database connection error, is the db down? Plesase check user and password too"
        super(ConnectionLost, self).__init__(self.name, msg)

