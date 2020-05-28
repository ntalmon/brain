from .reader import Reader
from .server_agent import ServerAgent
from ..utils.common import get_logger

logger = get_logger(__name__)


def upload_sample(host: str, port: int, path: str):
    """
    Read snapshots from sample file and stream them one by one to the server.

    :param host: hostname of the server
    :param port: port number of the server
    :param path: path of the sample file
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
