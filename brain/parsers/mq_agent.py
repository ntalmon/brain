from brain.utils.common import get_logger
from brain.utils.rabbitmq import RabbitMQ

logger = get_logger(__name__)


class MQAgent:
    def __init__(self, url):
        logger.info(f'connecting to mq: {url=}')
        self.utils = RabbitMQ(url)

    def consume_snapshots(self, callback, topic):
        self.utils.consume(callback, 'snapshot', [topic])

    def publish_result(self, result, topic):
        self.utils.publish(result, exchange='saver', queue=f'saver_{topic}')
