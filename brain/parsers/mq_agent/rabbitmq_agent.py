"""
The RabbitMQ agent module provides a MQ agent with RabbitMQ implementation.
"""

import json

from brain.parsers.mq_agent.base_mq_agent import BaseMQAgent
from brain.utils.common import get_logger
from brain.utils.rabbitmq import RabbitMQ

logger = get_logger(__name__)


class MQAgent(BaseMQAgent):
    """
    RabbitMQ-based implementation of MQ agent.
    """

    def __init__(self, url: str):
        BaseMQAgent.__init__(self, url)
        logger.info(f'connecting to mq: {url=}')
        self.utils = RabbitMQ(url)

    def consume_snapshots(self, callback: callable, topic: str):
        self.utils.consume(callback, 'snapshot', [topic])

    def publish_result(self, result: dict, topic: str):
        # convert result to JSON format and publish to MQ
        result = json.dumps(result)
        self.utils.publish(result, exchange='saver', queue=f'saver_{topic}')
