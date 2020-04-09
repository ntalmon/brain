"""
TODO: implement protocol separately
"""
from brain.client.reader import MindReader
from brain.protocol import ClientAgent


def construct_agent_snapshot(sample_snapshot, config):
    """
    Given a snapshot in sample format, and a configuration
    given by the server, construct a new snapshot in the
    agent's format, while tasking into consideration the
    configuration fields.
    TODO: implement
    """
    pass


def upload_sample(host, port, path):
    """
    TODO: add connection to server and upload sample
    """
    reader = MindReader(path)
    reader.load()
    agent = ClientAgent(host, port)
    config = agent.get_config()  # TODO: process snapshots according to config
    for snapshot in reader:
        agent_snapshot = construct_agent_snapshot(snapshot, config)
        agent.send_snapshot(agent_snapshot)
