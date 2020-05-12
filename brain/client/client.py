from brain.client.reader import Reader
from .server_agent import ServerAgent


def upload_sample(host, port, path):
    reader = Reader(path)
    user = reader.load()
    agent = ServerAgent(host, port)
    for snapshot in reader:
        agent.send_snapshot(user, snapshot)
    print('All snapshots uploaded successfully')
