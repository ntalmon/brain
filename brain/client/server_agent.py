"""
TODO: use design pattern for client agents
"""
import requests
from furl import furl

from brain.autogen import protocol_pb2


def copy_protobuf(item_a, item_b, attrs):
    for attr in attrs:
        setattr(item_a, attr, getattr(item_b, attr))


def construct_agent_snapshot(user, snapshot):
    agent_snapshot = protocol_pb2.Snapshot()
    copy_protobuf(agent_snapshot, snapshot, ['datetime'])
    copy_protobuf(agent_snapshot.user, user, ['user_id', 'username', 'birthday', 'gender'])
    copy_protobuf(agent_snapshot.pose.translation, snapshot.pose.translation, ['x', 'y', 'z'])
    copy_protobuf(agent_snapshot.pose.rotation, snapshot.pose.rotation, ['x', 'y', 'z', 'w'])
    copy_protobuf(agent_snapshot.color_image, snapshot.color_image, ['width', 'height', 'data'])
    copy_protobuf(agent_snapshot.feelings, snapshot.feelings, ['hunger', 'thirst', 'exhaustion', 'happiness'])
    return agent_snapshot


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
            return None  # TODO: handle this case
