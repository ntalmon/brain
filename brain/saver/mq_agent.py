from brain.utils.common import get_logger
from brain.utils.rabbitmq import RabbitMQ

logger = get_logger(__name__)


class MQAgent:
    def __init__(self, url):
        logger.info(f'initializing mq agent: {url=}')
        self.utils = RabbitMQ(url)

    def consume_results(self, callback, topics):
        def callback_wrapper(queue, data):
            topic = queue[len('saver_'):]
            logger.debug(f'consumed new results: {topic=}')
            return callback(topic, data)

        self.utils.consume(callback_wrapper, 'saver', [f'saver_{topic}' for topic in topics], exchange_type='direct')
