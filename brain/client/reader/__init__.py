"""
The reader package contains an interface for reading the sample file and get the parsed snapshots.
"""

from brain.utils.common import get_logger, get_file_stream_type
from brain.utils.consts import MessageFormat, FileFormat
from .mind_reader import MindReader

logger = get_logger(__name__)


def get_reader_type(msg_fmt):
    if msg_fmt == MessageFormat.MIND.value:
        return MindReader
    raise NotImplementedError(f'Unsupported message format: {msg_fmt}')


class Reader:
    """
    The reader class provides the reader functionality.
    It uses the driver design pattern in order and leaves the actual reading and parsing implementation to dedicated
    the dedicated reader drivers.

    The driver usage is:

    - After initializing the reader, the user will be available in the `user` member (`reader.user`).
    - In order to get the parsed snapshots, you should iterate over the reader object.

    :param path: path of the sample file.
    :param file_fmt: file format of the sample file.
    :param msg_fmt: the message format of the sample file (mind for example).
    """

    def __init__(self, path: str, file_fmt: FileFormat, msg_fmt: MessageFormat):
        file_stream_type = get_file_stream_type(file_fmt)
        # initialize file stream
        self.file_stream = file_stream_type(path, 'rb')
        reader_type = get_reader_type(msg_fmt)
        self._reader = reader_type(self.file_stream)
        try:
            # read header (user)
            self.user = self._reader.read_user()
        except Exception:
            self.file_stream.close()
            raise

    def __iter__(self):
        return self

    def __next__(self):
        try:
            # read next snapshot
            snapshot = self._reader.read_snapshot()
        except Exception:
            self.file_stream.close()
            raise

        if not snapshot:
            # reached end of file
            raise StopIteration
        return snapshot
