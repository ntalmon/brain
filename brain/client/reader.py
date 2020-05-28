"""
The reader module contains an interface for reading the sample file and get the parsed snapshots.
"""

import gzip
import struct

from brain.autogen import sample_pb2
from brain.utils.common import get_logger

logger = get_logger(__name__)


class Reader:
    """
    The Reader class reads and parses snapshots from a sample file.

    After initialization, you should load the reader via `reader.load()`, which will also return the parsed header.
    Then you can get the parsed snapshots by iterating over the reader object. Each iteration will read the next
    snapshot from the file and return the parsed snapshot:

    .. code-block:: python

        reader = Reader('sample.mind.gz')
        user = reader.load()
        for snapshot in reader:
            print(snapshot.uuid)

    :param path: sample file path
    """

    def __init__(self, path: str):
        logger.info(f'initializing reader: {path=}')
        self.path = path
        self.file_reader = None
        self.user = None  #
        self._loaded = False

    def _read_message(self):
        size_raw = self.file_reader.read(4)
        if not size_raw:
            return b''
        size, = struct.unpack('I', size_raw)
        msg = self.file_reader.read(size)
        if len(msg) != size:
            self.file_reader.close()
            logger.error(f'invalid file format: expected to reader {size} bytes, but read only {len(msg)}')
            raise Exception(f'Invalid file format: expected to read {size} bytes, but read only {len(msg)}')
        return msg

    def load(self) -> sample_pb2.User:
        """
        | Loads the sample file and reads.
        | Must be called before iterating over the reader.

        :return: the sample file header - the user.
        """
        logger.info(f'loading reader')
        if self._loaded:
            return self.user
        try:
            self.file_reader = gzip.open(self.path, 'rb')  # TODO: should this be configuration dependent?
        except OSError as error:
            logger.error(f'could not open {self.path}: error={error.strerror}')
            raise
        msg_user = self._read_message()
        if not msg_user:
            logger.error(f'invalid file format, missing header')
            raise Exception('Invalid file format, missing header')
        try:
            user = sample_pb2.User()
            user.ParseFromString(msg_user)
        except Exception:
            logger.error(f'invalid file format, failed to parser protobuf')
            print(f'Invalid file format: failed to parse protobuf')
            raise
        self._loaded = True
        self.user = user
        return user

    def __iter__(self):
        return self

    def __next__(self):
        if not self._loaded:
            logger.warning(f'reader is unloaded, cannot read snapshots, use reader.load() before')
            raise Exception('Reader is unloaded, cannot read snapshots, use reader.load() before')

        msg_snapshot = self._read_message()
        if not msg_snapshot:
            logger.info('reached end of snapshots file')
            self.file_reader.close()
            raise StopIteration

        snapshot = sample_pb2.Snapshot()
        snapshot.ParseFromString(msg_snapshot)
        return snapshot
