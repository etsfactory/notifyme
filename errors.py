import socket
import traceback as tb
from datetime import datetime
from raccoon import Publisher

import settings as st

# from connectors.rabbitmq import RabbitMQPublisher


# String format to log when an unhandled Exception is raised
# {m}   will be replaced by the Exception's message
# {t}   will be replaced by the Exception type
# {tb}  will be replaced by the execution traceback
ERROR_FORMAT = 'Unhandled {t}: {m}\nTraceback:\n{tb}'

def log_unhandled_exception(exc_type, exc_value, exc_tb):
        process_exception(exc_value, exc_tb=exc_tb)

def process_exception(exception, excepcion_type=None, msg=None, exc_tb=None, body=None):
    try:
        if not excepcion_type:
            exc_type = type(exception).__name__
        else:
            exc_type = excepcion_type

        if not msg:
            message = str(exception)
        else:
            message = msg

        if exc_tb is None:
            exc_tb = tb.format_exc()

        if not isinstance(exc_tb, str):
            exc_tb = ''.join(tb.format_tb(exc_tb))

        log_exception(exc_type, message, exc_tb, body)

        msg = {

            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "app_name": st.APP_NAME,
            "server": socket.gethostname(),
            "message": message,
            "type": exc_type,
        }
        if body:
            msg.update({
                "tag": 'Message received involved in the error: ' + str(body),
        })
        
        with Publisher(st.RABBITMQ_SERVER, st.RABBITMQ_USER, st.RABBITMQ_PASSWORD, 'nerrors', exchange_type='direct') as bus:
            bus.publish_msg(msg)
            

    except:
        st.logger.error('Error while processing another error')

def log_exception(exc_type, exc_value, exc_tb, body=None):

    try:

        msg = '\nBody: {}\n'.format(body) if body is not None else ''

        msg += ERROR_FORMAT
        msg = msg.replace('{t}', exc_type)
        msg = msg.replace('{m}', str(exc_value))
        msg = msg.replace('{tb}', exc_tb)

        st.logger.error(msg)
    
    except:
        st.logger.error('Error while loggin another error')
