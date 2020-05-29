"""
The MQ agent provides an interface for the saver to consume results from the MQ.
"""

from brain.utils.common import get_logger
from brain.utils.rabbitmq import RabbitMQ

logger = get_logger(__name__)


class MQAgent:
    """
    The MQ agent class connects to the MQ and allows to consume results on multiple topic.

    :param url: the MQ address.
    """

    def __init__(self, url: str):
        logger.info(f'initializing mq agent: {url=}')
        self.utils = RabbitMQ(url)

    def consume_results(self, callback: callable, topics: list):
        """
        Consume results from multiple topics.

        :param callback: will be called when a new message has arrived, with the message and the topic name.
        :param topics: topics to consume.
        """

        def callback_wrapper(queue, data):
            topic = queue[len('saver_'):]
            logger.debug(f'consumed new results: {topic=}')
            return callback(topic, data)

        self.utils.consume(callback_wrapper, 'saver', [f'saver_{topic}' for topic in topics], exchange_type='direct')
