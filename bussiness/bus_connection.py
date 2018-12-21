"""
Bus connection handler
"""
import queue
from jinja2 import Template, Undefined
from raccoon import Consumer

import settings as st

from connectors.smtp import SMTPHandler

from bussiness.users import UsersHandler
from bussiness.bus_filters import BusFiltersHandler
from bussiness.subscriptions import SubscriptionsHandler
from bussiness.templates import TemplatesHandler


class BusConnectionHandler():
    """
    Bus connection class
    """

    def __init__(self, subscriptions):
        self.subscriptions = subscriptions
        self.users = []
        self.filters_handler = BusFiltersHandler()
        self.subscriptions_handler = SubscriptionsHandler()
        self.users_handler = UsersHandler()
        self.templates_handler = TemplatesHandler()
        self.smtp = SMTPHandler(
            st.SMTP_EMAIL, st.SMTP_PASS, st.SMTP_HOST, st.SMTP_PORT)

    def start(self):
        """
        Starts the thread
        """
        if self.subscriptions:
            error = queue.Queue()
            self.bus_thread = Consumer(
                self.on_message,
                st.RABBITMQ_SERVER,
                st.RABBITMQ_USER,
                st.RABBITMQ_PASSWORD,
                self.subscriptions,
                st.RABBITMQ_QUEUE,
                error)

            self.bus_thread.start()

    def stop(self):
        """
        Stops the thread
        """
        self.bus_thread.stop()
        self.bus_thread.join()

    def on_message(self, message):
        """"
        When a message is received
        """
        if st.SEND_EMAILS:
            bus_filter = self.filters_handler.get_by_exchange_key(message.get(
                'metadata').get('exchange'), message.get('metadata').get('routing_key', ''))
            if bus_filter:
                for sub in self.subscriptions_handler.get_by_filter(
                        bus_filter):
                    user = self.users_handler.get(sub['user_id'])
                    template = self.templates_handler.get(sub['template_id'])

                    if template:
                        if not template.get('subject'):
                            subject = ''
                        else:
                            subject_t = Template(
                                template.get('subject'), undefined=SilentUndefined)
                            subject = subject_t.render(message)

                        text_t = Template(
                            template.get('text'),
                            undefined=SilentUndefined)
                        text = text_t.render(message)

                        user_filter = template.get('user_filter')
                        if user_filter:
                            user_name = message.get(user_filter)
                            user_searched = self.users_handler.get(
                                user_name)
                            if user_searched:
                                st.logger.info(
                                    'Notification to: %r', user_searched['email'])
                                self.smtp.send(
                                    user_searched['email'], subject, text)
                        else:
                            st.logger.info(
                                'Notification to: %r', user['email'])
                            self.smtp.send(user['email'], subject, text)

    def set_subscriptions(self, subscriptions):
        """
        Change subscriptions
        """
        self.subscriptions = subscriptions

    def unbind(self, exchange, key):
        """
        Unbind the queue from exchange and key
        """
        self.bus_thread.unbind_queue(exchange, key)


class SilentUndefined(Undefined):
    """
    Sorry about that. This class is created becasuse Jinja2 templates
    raises error on undefined variables. This is a little hack to replace
    undefined values with empty string
    """

    def _fail_with_undefined_error(self, *args, **kwargs):
        return ''

    __add__ = __radd__ = __mul__ = __rmul__ = __div__ = __rdiv__ = \
        __truediv__ = __rtruediv__ = __floordiv__ = __rfloordiv__ = \
        __mod__ = __rmod__ = __pos__ = __neg__ = __call__ = \
        __getitem__ = __lt__ = __le__ = __gt__ = __ge__ = __int__ = \
        __float__ = __complex__ = __pow__ = __rpow__ = \
        _fail_with_undefined_error
