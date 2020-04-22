from brain.client.mind import MindReader
from brain.client.server_agent import get_server_agent, construct_server_snapshot


def upload_sample(host, port, path):
    reader = MindReader(path)
    user = reader.load()
    agent = get_server_agent(host, port)
    for snapshot in reader:
        agent_snapshot = construct_server_snapshot(user, snapshot)
        agent.send_snapshot(agent_snapshot)
