"""
The base reader module provides an abstract class for reader drivers.
"""

import abc


class BaseReader(abc.ABC):
    """
    The base reader abstract class should be inherited and implemented by reader drivers.

    :param file_stream: file stream of the sample file.
    """

    def __init__(self, file_stream):
        self.file_stream = file_stream

    @abc.abstractmethod
    def read_user(self):
        """
        Read and parse the user from the sample file.

        :return: the parsed user as python object.
        """

        pass

    @abc.abstractmethod
    def read_snapshot(self):
        """
        Read and parse the next snapshot from the sample file.

        :return: the parsed snapshot as python object
        """

        pass
