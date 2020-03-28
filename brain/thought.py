import datetime
import struct


class Thought:
    def __init__(self, user_id, timestamp, thought):
        self.user_id = user_id
        self.timestamp = timestamp
        self.thought = thought

    def __repr__(self):
        return f'Thought(user_id={self.user_id}, timestamp={self.timestamp!r}, thought={self.thought!r})'

    def __str__(self):
        return f'[{self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}] user {self.user_id}: {self.thought}'

    def __eq__(self, other):
        if not isinstance(other, Thought):
            return False
        return self.user_id == other.user_id and self.timestamp == other.timestamp and self.thought == other.thought

    def serialize(self):
        ts = int(self.timestamp.timestamp())
        hdr = struct.pack('LLI', self.user_id, ts, len(self.thought))
        return hdr + self.thought.encode()

    @classmethod
    def deserialize(cls, data):
        user_id, ts, _ = struct.unpack('LLI', data[:20])
        ts = datetime.datetime.fromtimestamp(ts)
        thought = data[20:].decode()
        return Thought(user_id, ts, thought)
