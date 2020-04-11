import json
from google.protobuf import json_format

from brain.server.client_agent import HTTPAgent

agents = {
    'http': HTTPAgent
}


def get_client_agent():
    protocol = 'http'  # TODO: extract from config
    if protocol not in agents:
        return None  # TODO: handle this case
    return agents[protocol]()


agent = get_client_agent()


def handle_color_image(snapshot_dict):
    pass


def handle_depth_image(snapshot_dict):
    pass


def construct_json(snapshot):
    snapshot_dict = json_format.MessageToDict(snapshot)
    if 'color_image' in snapshot_dict:
        handle_color_image(snapshot_dict)
    if 'depth_image' in snapshot_dict:
        handle_depth_image(snapshot_dict)
    return json.dumps(snapshot_dict)


@agent.snapshot_handler
def handle_snapshot(snapshot):
    """
    TODO: move to protocol format
    """
    json_snapshot = construct_json(snapshot)
    agent.publish(json_snapshot)


def run_server(host, port, publish):
    """
    TODO: handle publish
    """
    agent.publish = publish
    agent.run(host, port)
