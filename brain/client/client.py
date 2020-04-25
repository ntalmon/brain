from brain.client.reader import Reader
from .server_agent import ServerAgent, construct_server_snapshot


def upload_sample(host, port, path):
    reader = Reader(path)
    user = reader.load()
    agent = ServerAgent(host, port)
    for snapshot in reader:
        agent_snapshot = construct_server_snapshot(user, snapshot)
        agent.send_snapshot(agent_snapshot)
