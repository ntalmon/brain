"""
The base MQ agent module provides an abstract class for MQ agent implementations.
"""

import abc

from brain.autogen import server_parsers_pb2


class BaseMQAgent(abc.ABC):
    """
    The base MQ agent abstract class should be inherited and implemented by MQ agents.

    :param url: MQ address.
    """

    def __init__(self, url: str):
        self.url = url

    @abc.abstractmethod
    def publish_snapshot(self, snapshot: server_parsers_pb2.Snapshot):
        """
        Publish snapshot to the parsers via the MQ.

        :param snapshot: snapshot to send in server_parsers_pb2.Snapshot format.
        """

        pass
