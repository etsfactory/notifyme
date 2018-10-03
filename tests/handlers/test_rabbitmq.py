from notify_me.handlers.rabbitmq import RabbitMqHandler

def test_rabbitmq_init():
    rabbit = RabbitMqHandler('localhost')
    assert rabbit is not None
