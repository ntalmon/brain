"""
The MQ agent provides an interface for the parsers to communicate with the MQ.
"""

from brain.utils.common import get_logger
from brain.utils.rabbitmq import RabbitMQ

logger = get_logger(__name__)


class MQAgent:
    """
    The MQ agent class contains:

    - Consuming the MQ on a dedicated topic (running parser as a service)
    - Publish result to the saver on a dedicated topic.

    :param url: address of the MQ.
    """

    def __init__(self, url: str):
        logger.info(f'connecting to mq: {url=}')
        self.utils = RabbitMQ(url)

    def consume_snapshots(self, callback: callable, topic: str):
        """
        Consume snapshots on a dedicated topic.

        :param callback: will be called when a new message arrives.
        :param topic: the topic of the consumer - used to identify the relevant parser.
        """

        self.utils.consume(callback, 'snapshot', [topic])

    def publish_result(self, result: str, topic: str):
        """
        Publish parsing result to the saver on a dedicated topic.

        :param result: the result to publish.
        :param topic: the topic of the publisher (used by the server to identify the result type).
        """

        self.utils.publish(result, exchange='saver', queue=f'saver_{topic}')
