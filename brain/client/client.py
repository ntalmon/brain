"""
TODO: implement protocol separately
TODO: (optionally) move server agent(s) to a sub-package
"""
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


def upload_sample(host, port, path):
    """
    TODO: add connection to server and upload sample
    """
    reader = MindReader(path)
    reader.load()
    agent = get_server_agent(host, port)
    for snapshot in reader:
        agent_snapshot = snapshot  # TODO: manipulate agent snapshot if needed
        agent.send_snapshot(agent_snapshot)
