"""
TODO: handle readers design
"""
import gzip
import struct

from brain.autogen import reader_pb2


class Reader:
    def __init__(self, path):
        self.path = path
        self.file_reader = None
        self.user = None
        self._loaded = False

    def _read_message(self):
        size_raw = self.file_reader.read(4)
        if not size_raw:
            return b''
        size, = struct.unpack('I', size_raw)
        msg = self.file_reader.read(size)
        if len(msg) != size:
            self.file_reader.close()
            raise Exception('Invalid file format')
        return msg

    def load(self):
        if self._loaded:
            return
        self.file_reader = gzip.open(self.path, 'rb')  # TODO: should this be configuration dependent?
        msg_user = self._read_message()
        user = reader_pb2.User()
        user.ParseFromString(msg_user)
        self._loaded = True
        return user

    def __iter__(self):
        return self

    def __next__(self):
        if not self._loaded:
            return  # TODO: handle this case by message/exception

        msg_snapshot = self._read_message()
        if not msg_snapshot:  # TODO: check how we make sure we ended read the file
            self.file_reader.close()
            raise StopIteration

        snapshot = reader_pb2.Snapshot()
        snapshot.ParseFromString(msg_snapshot)
        return snapshot
