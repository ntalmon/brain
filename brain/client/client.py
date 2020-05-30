"""
The client module contains the main logic of the client via `upload_sample`.
"""

from brain.utils.common import get_logger
from brain.utils.consts import config
from .reader import Reader
from .server_agent import load_server_agent

logger = get_logger(__name__)


def upload_sample(host: str, port: int, path: str) -> int:
    """
    Reads the sample file and streams the snapshots to the server.

    :param host: server hostname.
    :param port: server port number.
    :param path: sample file path.
    :return: number of uploaded snapshots.
    """

    # initialize reader
    logger.info(f'uploading samples to {host}:{port} from {path=}')
    file_fmt = config['sample_format']['file_format']
    msg_fmt = config['sample_format']['message_format']
    reader = Reader(path, file_fmt, msg_fmt)
    user = reader.user

    # initialize server agent
    protocol = config['client_server_protocol']
    server_agent_module = load_server_agent(protocol)
    server_agent = server_agent_module.ServerAgent(host, port)

    count = 0
    for snapshot in reader:
        logger.debug(f'uploading snapshot #{count} to server')
        # construct snapshot and send
        server_snapshot = server_agent.construct_snapshot(user, snapshot)
        server_agent.send_snapshot(server_snapshot)
        count += 1

    logger.info(f'all {count} snapshots were successfully uploaded')
    return count
