"""
The RabbitMQ agent module provides a MQ agent with RabbitMQ implementation.
"""
from brain.saver.mq_agent.base_mq_agent import BaseMQAgent
from brain.utils.common import get_logger
from brain.utils.rabbitmq import RabbitMQ

logger = get_logger(__name__)


class MQAgent(BaseMQAgent):
    """
    RabbitMQ-based implementation of MQ agent.
    """

    def __init__(self, url: str):
        BaseMQAgent.__init__(self, url)
        logger.info(f'initializing mq agent: {url=}')
        self.utils = RabbitMQ(url)

    def consume_results(self, callback: callable, topics: list):
        def callback_wrapper(queue, data):
            topic = queue[len('saver_'):]  # parsers-saver queue convention is <topic>_saver
            logger.debug(f'consumed new results: {topic=}')
            return callback(topic, data)

        # consume in 'direct' exchange - publisher also provides queue name in addition to exchange,
        # and the message will be sent to the specific queue consumer in this exchange.
        self.utils.consume(callback_wrapper, 'saver', [f'saver_{topic}' for topic in topics], exchange_type='direct')
