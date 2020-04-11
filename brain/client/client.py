"""
TODO: implement protocol separately
TODO: (optionally) move server agent(s) to a sub-package
"""
from brain.autogen import protocol_pb2
from brain.client.reader import MindReader
from brain.client.server_agent import HTTPServerAgent

agents = {
    'http': HTTPServerAgent
}


def get_server_agent(host, port):
    protocol = 'http'  # TODO: extract from config
    if protocol not in agents:
        return None  # TODO: handle this case
    return agents[protocol](host, port)


def copy_protobuf(item_a, item_b, attrs):
    for attr in attrs:
        setattr(item_a, attr, getattr(item_b, attr))


def construct_agent_snapshot(user, snapshot):
    """
    TODO: should this method move to server agent?
    """
    agent_snapshot = protocol_pb2.Snapshot()
    copy_protobuf(agent_snapshot, snapshot, ['datetime'])
    copy_protobuf(agent_snapshot.user, user, ['user_id', 'username', 'birthday', 'gender'])
    copy_protobuf(agent_snapshot.pose.translation, snapshot.pose.translation, ['x', 'y', 'z'])
    copy_protobuf(agent_snapshot.pose.rotation, snapshot.pose.rotation, ['x', 'y', 'z', 'w'])
    copy_protobuf(agent_snapshot.color_image, snapshot.color_image, ['width', 'height', 'data'])
    copy_protobuf(agent_snapshot.feelings, snapshot.feelings, ['hunger', 'thirst', 'exhaustion', 'happiness'])
    return agent_snapshot


def upload_sample(host, port, path):
    reader = MindReader(path)
    user = reader.load()
    agent = get_server_agent(host, port)
    for snapshot in reader:
        agent_snapshot = construct_agent_snapshot(user, snapshot)
        agent.send_snapshot(agent_snapshot)
