"""
TODO: (optionally) move server agent(s) to a sub-package
"""
from brain.client.reader import MindReader
from brain.client.server_agent import HTTPServerAgent, construct_agent_snapshot
from brain.utils.config import client_config

agents = {
    'http': HTTPServerAgent
}


def get_server_agent(host, port):
    protocol = client_config['server_protocol']
    if protocol not in agents:
        raise Exception(f'Invalid clint-server protocol given: {protocol}')
    return agents[protocol](host, port)


def upload_sample(host, port, path):
    reader = MindReader(path)
    user = reader.load()
    agent = get_server_agent(host, port)
    for snapshot in reader:
        agent_snapshot = construct_agent_snapshot(user, snapshot)
        agent.send_snapshot(agent_snapshot)
