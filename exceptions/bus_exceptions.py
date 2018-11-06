import settings as st

class BusException(Exception):
    def __init__(self, msg, original_exception):
        st.logger.error('Error in the bus connection')
        super(BusException, self).__init__(msg + (": %s" % original_exception))
        self.original_exception = original_exception
    
class ConnectionErrorException(BusException):
    """Basic exception for errors raised by inserting into the database"""
    def __init__(self, msg=None):
        if msg is None:
            msg = "The bus connection is closed"
        super(ConnectionErrorException, self).__init__(msg)

