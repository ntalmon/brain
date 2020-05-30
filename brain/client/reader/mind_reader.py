"""
The mind reader module contains the reader driver for the mind format.
"""

import struct

from brain.autogen import mind_pb2
from brain.client.reader.base_reader import BaseReader
from brain.utils.common import parse_protobuf


class MindReader(BaseReader):
    """
    The mind reader class inherits the BaseReader abstract class and implements the mind reader driver.
    """

    def _read_msg(self):
        # read 4 bytes of message size
        size = self.file_stream.read(4)
        if not size:
            return b''

        ln = len(size)
        if ln != 4:
            raise ValueError(f'Invalid file format: expected to read 4 bytes header, but only {ln} were read')
        size, = struct.unpack('I', size)

        # read <size> bytes of the message
        msg = self.file_stream.read(size)
        ln = len(msg)
        if ln < size:
            raise ValueError(f'Invalid file format: expected to read {size} bytes message, but only {ln} were read')

        return msg

    def read_user(self) -> mind_pb2.User:
        """
        Read message from the sample file and parse it as user message.

        :return: the parsed user as mind_pb2.User object.
        :raises: ValueError for invalid file format.
        """

        msg = self._read_msg()
        if not msg:
            raise ValueError(f'Invalid file format: reached EOF before reading the user')

        user = parse_protobuf(mind_pb2.User(), msg)
        return user

    def read_snapshot(self) -> mind_pb2.Snapshot:
        """
        Read message from the sample file and parse it as snapshot message.

        :return: the parsed snapshot as mind_pb2.Snapshot object.
        """

        msg = self._read_msg()
        if not msg:
            return None

        return parse_protobuf(mind_pb2.Snapshot(), msg)
