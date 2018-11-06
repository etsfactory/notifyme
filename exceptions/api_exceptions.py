import settings as st

class DBException(Exception):
    def __init__(self, msg, original_exception):
        st.logger.error('Error in the database')
        super(DBException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception
    
class WriteError(DBException):
    """Basic exception for errors raised by inserting into the database"""
    def __init__(self, msg=None):
        if msg is None:
            msg = "An error occured inserting into database"
        super(WriteError, self).__init__(msg)

class ReadError(DBException):
    """Basic exception for errors raised by reading from the database"""
    def __init__(self, msg=None):
        if msg is None:
            msg = "An error occured reading from the database"
        super(ReadError, self).__init__(msg)
