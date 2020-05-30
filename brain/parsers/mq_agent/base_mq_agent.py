"""
The base MQ agent provides an abstract class for MQ agent implementations.
"""

import abc


class BaseMQAgent(abc.ABC):
    """
    The MQ agent abstract class contains should be inherited and implemented by MQ agents.

    :param url: address of the MQ.
    """

    def __init__(self, url: str):
        self.url = url

    @abc.abstractmethod
    def consume_snapshots(self, callback: callable, topic: str):
        """
        Consume snapshots on a dedicated topic.

        :param callback: will be called when a new message arrives.
        :param topic: the topic of the consumer - used to identify the relevant parser.
        """

        pass

    @abc.abstractmethod
    def publish_result(self, result: dict, topic: str):
        """
        Publish parsing result to the saver on a dedicated topic.

        :param result: the result to publish (python object).
        :param topic: the topic of the publisher (used by the server to identify the result type).
        """

        pass
