"""
The http server agent module provides a server agent of http protocol.
"""

from furl import furl

from brain.autogen import client_server_pb2, mind_pb2
from brain.client.server_agent.base_server_agent import BaseServerAgent
from brain.utils.common import get_logger, serialize_protobuf
from brain.utils.http import post

logger = get_logger(__name__)


def copy_protobuf(item_a, item_b, attrs):
    for attr in attrs:
        setattr(item_a, attr, getattr(item_b, attr))


class ServerAgent(BaseServerAgent):
    """
    HTTP-based implementation of server agent.
    """

    def __init__(self, host: str, port: int):
        BaseServerAgent.__init__(self, host, port)
        logger.info(f'initializing ServerAgent, {host=}, {port=}')
        self.url = furl(scheme='http', host=host, port=port)

    @classmethod
    def _construct_snapshot(cls, user: mind_pb2.User, snapshot: mind_pb2.Snapshot) -> client_server_pb2.Snapshot:
        new_snapshot = client_server_pb2.Snapshot()
        copy_protobuf(new_snapshot, snapshot, ['datetime'])
        copy_protobuf(new_snapshot.user, user, ['user_id', 'username', 'birthday', 'gender'])
        copy_protobuf(new_snapshot.pose.translation, snapshot.pose.translation, ['x', 'y', 'z'])
        copy_protobuf(new_snapshot.pose.rotation, snapshot.pose.rotation, ['x', 'y', 'z', 'w'])
        copy_protobuf(new_snapshot.color_image, snapshot.color_image, ['width', 'height', 'data'])
        copy_protobuf(new_snapshot.depth_image, snapshot.depth_image, ['width', 'height'])
        new_snapshot.depth_image.data.extend(snapshot.depth_image.data)
        copy_protobuf(new_snapshot.feelings, snapshot.feelings, ['hunger', 'thirst', 'exhaustion', 'happiness'])
        return new_snapshot

    def send_snapshot(self, user: mind_pb2.User, snapshot: mind_pb2.Snapshot):
        url = self.url / 'snapshot'
        server_snapshot = self._construct_snapshot(user, snapshot)
        snapshot_msg = serialize_protobuf(server_snapshot)
        logger.debug(f'sending snapshot to {url}')
        post(url, snapshot_msg)
