from notify_me.connectors.rabbitmq import RabbitMqHandler

def test_rabbitmq_init():
    rabbit = RabbitMqHandler('localhost', 'hello', 'direct_logs')
    assert rabbit is not None
