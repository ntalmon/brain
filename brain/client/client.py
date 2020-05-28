"""
The client module contains the main logic of the client via `upload_sample`.
"""

from .reader import Reader
from .server_agent import ServerAgent
from ..utils.common import get_logger

logger = get_logger(__name__)


def upload_sample(host: str, port: int, path: str):
    """
    Reads the sample file and streams the snapshots to the server.

    :param host: server hostname.
    :param port: server port number.
    :param path: sample file path.
    """

    logger.info(f'uploading samples to {host}:{port} from {path=}')
    reader = Reader(path)
    user = reader.load()
    agent = ServerAgent(host, port)
    count = 0
    for snapshot in reader:
        logger.debug(f'sending snapshot #{count} to server')
        agent.send_snapshot(user, snapshot)
        logger.debug(f'snapshot #{count} was successfully uploaded')
        count += 1
    logger.info(f'all {count} snapshots were successfully uploaded')
    print(f'All {count} snapshots successfully uploaded')
