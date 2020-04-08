"""
TODO: implement protocol separately
"""
from brain.client.reader import MindReader
from brain.protocol import ClientAgent


def upload_sample(host, port, path):
    """
    TODO: add connection to server and upload sample
    """
    reader = MindReader(path)
    reader.load()
    agent = ClientAgent(host, port)
    config = agent.get_config()  # TODO: process snapshots according to config
    for snapshot in reader:
        agent.send_snapshot(snapshot)
