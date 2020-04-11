"""
TODO: handle readers design
"""
import gzip
import struct

from brain.autogen import reader_pb2


class MessageReader:
    def __init__(self, reader):
        self.reader = reader

    def read_message(self):
        size_raw = self.reader.read(4)
        if not size_raw:
            return b''
        size, = struct.unpack('I', size_raw)
        msg = self.reader.read(size)
        if len(msg) != size:
            self.reader.close()
            raise Exception('Invalid file format')
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
        user = reader_pb2.User()
        user.ParseFromString(msg_user)
        self.user = user
        self._loaded = True
        return user

    def read_snapshot(self):
        if not self._loaded:
            return  # TODO: handle this case by message/exception
        msg_snapshot = self.msg_reader.read_message()
        snapshot = reader_pb2.Snapshot()
        snapshot.ParseFromString(msg_snapshot)
        return snapshot

    def __iter__(self):
        return self

    def __next__(self):
        if not self._loaded:
            return  # TODO: handle this case by message/exception

        msg_snapshot = self.msg_reader.read_message()
        if not msg_snapshot:  # TODO: check how we make sure we ended read the file
            self.file_obj.close()
            raise StopIteration

        snapshot = reader_pb2.Snapshot()
        snapshot.ParseFromString(msg_snapshot)
        return snapshot
