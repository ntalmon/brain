"""
The MQ agent module provides an interface for the server to communicate with the MQ.
"""

from brain.utils.common import get_logger
from brain.utils.rabbitmq import RabbitMQ

logger = get_logger(__name__)


class MQAgent:
    """
    The MQ agent class connect to the MQ and allows publishing snapshot to the MQ.
    """

    def __init__(self, url: str):
        logger.info(f'initializing mq agent: {url=}')
        self.utils = RabbitMQ(url)

    def publish_snapshot(self, snapshot: bytes):
        """
        Publish snapshot to the parsers via the MQ.

        :param snapshot: serialized snapshot.
        """

        self.utils.publish(snapshot, exchange='snapshot')
