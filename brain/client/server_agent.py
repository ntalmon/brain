from furl import furl

from brain.autogen import protocol_pb2
from brain.utils.http import post


def copy_protobuf(item_a, item_b, attrs):
    for attr in attrs:
        setattr(item_a, attr, getattr(item_b, attr))


class ServerAgent:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = furl(scheme='http', host=host, port=port)

    @classmethod
    def _construct_snapshot(cls, user, snapshot):
        new_snapshot = protocol_pb2.Snapshot()
        copy_protobuf(new_snapshot, snapshot, ['datetime'])
        copy_protobuf(new_snapshot.user, user, ['user_id', 'username', 'birthday', 'gender'])
        copy_protobuf(new_snapshot.pose.translation, snapshot.pose.translation, ['x', 'y', 'z'])
        copy_protobuf(new_snapshot.pose.rotation, snapshot.pose.rotation, ['x', 'y', 'z', 'w'])
        copy_protobuf(new_snapshot.color_image, snapshot.color_image, ['width', 'height', 'data'])
        copy_protobuf(new_snapshot.depth_image, snapshot.depth_image, ['width', 'height'])
        new_snapshot.depth_image.data.extend(snapshot.depth_image.data)
        copy_protobuf(new_snapshot.feelings, snapshot.feelings, ['hunger', 'thirst', 'exhaustion', 'happiness'])
        return new_snapshot

    def send_snapshot(self, user, snapshot):
        new_snapshot = self._construct_snapshot(user, snapshot)
        url = self.url / 'snapshot'
        snapshot_msg = new_snapshot.SerializeToString()
        status = post(url, snapshot_msg)
        if status != 200:
            raise Exception(f'Failed to send snapshot. Server returned with code {status}')
