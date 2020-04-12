"""
TODO: can we really need MQAgent layer and not using find_driver directly?
"""
from furl import furl

from .rabbitmq import RabbitMQAgent

drivers = {
    'rabbitmq': RabbitMQAgent
}


def find_driver(url):
    scheme = furl(url).scheme
    if scheme not in drivers:
        raise Exception(f'Invalid url: MQ scheme {scheme} is unsupported')
    return drivers[scheme]


class MQAgent:
    def __init__(self, url):
        agent_type = find_driver(url)
        self._agent = agent_type(url) if agent_type else None  # TODO: handle cases where agent is None

    def consume(self, callback, exchange='', queue=''):
        return self._agent.consume(callback, exchange=exchange, queue=queue)

    def multi_consume(self, callback, exchange='', queues=None):
        return self._agent.multi_consume(callback, exchange=exchange, queues=queues)

    def publish(self, data, exchange='', queue=''):
        return self._agent.publish(data, exchange=exchange, queue=queue)
