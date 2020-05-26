from brain.utils.common import get_logger
from brain.utils.rabbitmq import RabbitMQ

logger = get_logger(__name__)


class MQAgent:
    def __init__(self, url):
        logger.info(f'initializing mq agent: {url=}')
        self.utils = RabbitMQ(url)

    def publish_snapshot(self, snapshot):
        self.utils.publish(snapshot, exchange='snapshot')
