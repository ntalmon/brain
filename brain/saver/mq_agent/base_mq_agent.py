"""
The base MQ agent module provides an abstract class for MQ agent implementations.
"""

import abc


class BaseMQAgent(abc.ABC):
    """
    The base MQ agent abstract class should be inherited and implemented by MQ agents.

    :param url: MQ address.
    """

    def __init__(self, url: str):
        self.url = url

    def consume_results(self, callback: callable, topics: list):
        """
        Consume results from multiple topics.

        :param callback: will be called when a new message has arrived, with the message and the topic name.
        :param topics: topics to consume.
        """

        pass
