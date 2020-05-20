from .reader import Reader
from .server_agent import ServerAgent


def upload_sample(host: str, port: int, path: str):
    """
    Reads snapshots from file and streams them one by one to the server.
    :param host: hostname of the server
    :param port: port number of the server
    :param path: path of the sample file
    """
    reader = Reader(path)
    user = reader.load()
    agent = ServerAgent(host, port)
    for snapshot in reader:
        agent.send_snapshot(user, snapshot)
    print('All snapshots uploaded successfully')
