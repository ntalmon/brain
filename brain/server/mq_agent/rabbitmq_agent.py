"""
The RabbitMQ agent module provides a MQ agent with RabbitMQ implementation.
"""

import threading

from brain.autogen import server_parsers_pb2
from brain.server.mq_agent.base_mq_agent import BaseMQAgent
from brain.utils.common import get_logger, serialize_protobuf
from brain.utils.rabbitmq import RabbitMQ

logger = get_logger(__name__)


class MQAgent(BaseMQAgent):
    """
    RabbitMQ-based implementation of MQ agent.
    """

    def __init__(self, url: str):
        BaseMQAgent.__init__(self, url)
        logger.info(f'initializing mq agent: {url=}')
        self.mq_lock = threading.Lock()
        self.utils = RabbitMQ(self.url)

    def publish_snapshot(self, snapshot: server_parsers_pb2.Snapshot):
        snapshot_msg = serialize_protobuf(snapshot)
        # take a lock and send snapshot
        with self.mq_lock:
            self.utils.publish(snapshot_msg, exchange='snapshot')
