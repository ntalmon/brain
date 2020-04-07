"""
TODO: handle readers design
"""
import gzip
import struct

from . import brain_pb2


class MessageReader:
    def __init__(self, reader):
        self.reader = reader

    def read_message(self):
        size_raw = self.reader.read(4)
        size, = struct.unpack('I', size_raw)
        msg = self.reader.read(size)
        return msg


class MindReader:
    def __init__(self, path):
        self.path = path
        self.file_obj = None
        self.user = None
        self.msg_reader = None
        self._loaded = False

    def load(self):
        if self._loaded:
            return
        self.file_obj = gzip.open(self.path, 'rb')
        self.msg_reader = MessageReader(self.file_obj)
        msg_user = self.msg_reader.read_message()
        user = brain_pb2.User()
        user.ParseFromString(msg_user)
        self.user = user
        self._loaded = True
        return user

    def read_snapshot(self):
        if not self._loaded:
            return  # TODO: handle this case by message/exception
        msg_snapshot = self.msg_reader.read_message()
        snapshot = brain_pb2.Snapshot()
        snapshot.ParseFromString(msg_snapshot)
        return snapshot

    def read_snapshots(self):
        """
        TODO: implement
        """
        pass
