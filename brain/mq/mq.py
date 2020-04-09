from furl import furl

from .rabbitmq import RabbitMQAgent

drivers = {
    'rabbitmq': RabbitMQAgent
}


def find_driver(scheme):
    if scheme not in drivers:
        return None  # TODO: handle this case
    return drivers[scheme]


class MQAgent:
    def __init__(self, url):
        self.url = url
        _url = furl(url)
        agent_type = find_driver(furl.scheme)
        self._agent = agent_type(url) if agent_type else None  # TODO: handle cases where agent is None

    def consume(self, callback, exchange='', queue=''):
        self._agent.consume(callback, exchange=exchange, queue=queue)

    def publish(self, data, exchange='', queue=''):
        self._agent.publish(data, exchange=exchange, queue=queue)
