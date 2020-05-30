"""
The base server agent module provides an abstract class for server agent implementations.
"""

import abc

from brain.autogen import mind_pb2


class BaseServerAgent(abc.ABC):
    """
    The base server agent class should be inherited and implemented by server agents.

    :param host: server hostname.
    :param port: server port number.
    """

    def __init__(self, host, port):
        self.host = host
        self.port = port

    @abc.abstractmethod
    def send_snapshot(self, user: mind_pb2.User, snapshot: mind_pb2.Snapshot):
        """
        Constructs a message from the given user and snapshots and sends it to the server.

        :param user: user in mind_pb2.User format.
        :param snapshot: snapshot in mind_pb2.Snapshot format.
        """

        pass
