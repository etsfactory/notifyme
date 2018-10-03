import socket
import traceback as tb
from datetime import datetime

import settings as st

# String format to log when an unhandled Exception is raised
# {m}   will be replaced by the Exception's message
# {t}   will be replaced by the Exception type
# {tb}  will be replaced by the execution traceback
ERROR_FORMAT = 'Unhandled {t}: {m}\nTraceback:\n{tb}'


def log_unhandled_exception(exc_type, exc_value, exc_tb):
        process_exception(exc_value, exc_tb=exc_tb)


def process_exception(exception, exc_tb=None, body=None):
    try:
        if exc_tb is None:
            exc_tb = tb.format_exc()

        log_exception(type(exception), exception, exc_tb, body)

        msg = {

            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "app_name": st.APP_NAME,
            "server": socket.gethostname(),
            "message": str(exception),
            "stack": exc_tb,
            "type": type(exception).__name__,
        }
        if body:
            msg.update({
                "tag": 'Message received involved in the error: ' + str(body),
        })

        # with Publisher(st.BUS_HOST, st.BUS_USER, st.BUS_PASSWORD, st.EXCHANGE_OUT_ERROR) as bus:
        #    bus.publish_msg(msg)
    except:
        pass


def log_exception(exc_type, exc_value, exc_tb, body=None):

    try:

        if not isinstance(exc_tb, str):
            exc_tb = ''.join(tb.format_tb(exc_tb))

        msg = '\nBody: {}\n'.format(body) if body is not None else ''

        msg += ERROR_FORMAT
        msg = msg.replace('{t}', exc_type.__name__)
        msg = msg.replace('{m}', str(exc_value))
        msg = msg.replace('{tb}', exc_tb)

        st.logger.error(msg)
    except:
        pass
