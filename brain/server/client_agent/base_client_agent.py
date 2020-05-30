"""
The base client agent module provides an abstract class for client agent implementations.
"""

import abc


def empty_function(*args, **kwargs):
    pass


class BaseClientAgent(abc.ABC):
    """
    The base client agent abstract class should be inherited and implemented by client agents.

    :param publish: will be passed as a parameter when calling the snapshot handlers.
    """

    def __init__(self, publish: callable = empty_function):
        self.publish = publish or empty_function

    @abc.abstractmethod
    def register_snapshot_handler(self, handler: callable):
        """
        Register with the given snapshot handler: whenever a snapshot is received, the handler will be called with
        the parsed snapshot, and the publish function.

        :param handler: the handler function
        """

        pass

    @abc.abstractmethod
    def run(self, host: str, port: int):
        """
        Start running the server. It is the client agent responsibility to parse the messages
        and calling the snapshot handlers.

        :param host: hostname to listen.
        :param port: port number to listen
        """
        pass
