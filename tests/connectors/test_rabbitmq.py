from notify_me.connectors.rabbitmq import RabbitMqHandler


def test_rabbitmq_init():
    rabbit = RabbitMqHandler('localhost', 0, 'hello', 'direct_logs')
    assert rabbit is not None
