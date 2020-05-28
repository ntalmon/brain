"""
The API agent provides communication with the API.
It provides the api_get function to get data from the API.
"""
from brain.utils.common import get_logger
from brain.utils.http import get

logger = get_logger(__name__)


def api_get(host, port, path):
    """
    Get data from the API using a specific path.

    :param host: hostname of the API server
    :param port: port number of the API server
    :param path: relative path in the API (e.g. "/users/1/snapshots")
    :return: the returned result from the API, in json format
    """

    url = f'http://{host}:{port}/{path}'
    logger.info(f'getting data from api: GET {url}')
    result = get(url)
    return result
