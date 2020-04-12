"""
TODO: use design pattern for client agents
"""
import requests
from furl import furl

from brain.autogen import protocol_pb2


def copy_protobuf(item_a, item_b, attrs):
    for attr in attrs:
        setattr(item_a, attr, getattr(item_b, attr))


def construct_server_snapshot(user, snapshot):
    server_snapshot = protocol_pb2.Snapshot()
    copy_protobuf(server_snapshot, snapshot, ['datetime'])
    copy_protobuf(server_snapshot.user, user, ['user_id', 'username', 'birthday', 'gender'])
    copy_protobuf(server_snapshot.pose.translation, snapshot.pose.translation, ['x', 'y', 'z'])
    copy_protobuf(server_snapshot.pose.rotation, snapshot.pose.rotation, ['x', 'y', 'z', 'w'])
    copy_protobuf(server_snapshot.color_image, snapshot.color_image, ['width', 'height', 'data'])
    copy_protobuf(server_snapshot.depth_image, snapshot.depth_image, ['width', 'height'])
    server_snapshot.depth_image.data.extend(snapshot.depth_image.data)
    copy_protobuf(server_snapshot.feelings, snapshot.feelings, ['hunger', 'thirst', 'exhaustion', 'happiness'])
    return server_snapshot


class HTTPServerAgent:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = furl(scheme='http', host=host, port=port)

    def send_snapshot(self, snapshot):
        request = self.url / 'snapshot'
        snapshot_msg = snapshot.SerializeToString()
        response = requests.post(request, snapshot_msg)
        if response.status_code != 200:
            raise Exception()  # TODO: handle this case
