"""
TODO: use design pattern for client agents
"""
from brain.autogen import protocol_pb2
from brain.client.server_agent.http_server_agent import HTTPServerAgent
from brain.utils.config import client_config

agents = {
    'http': HTTPServerAgent
}


def get_server_agent(host, port):
    protocol = client_config['server_protocol']
    if protocol not in agents:
        raise Exception(f'Invalid clint-server protocol given: {protocol}')
    return agents[protocol](host, port)


def copy_protobuf(item_a, item_b, attrs):
    for attr in attrs:
        setattr(item_a, attr, getattr(item_b, attr))


def construct_server_snapshot(user, snapshot):
    # TODO: should this method be in specific agent context?
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
