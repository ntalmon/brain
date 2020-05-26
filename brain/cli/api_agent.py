from brain.utils.common import get_logger
from brain.utils.http import get

logger = get_logger(__name__)


def api_get(host, port, path):
    url = f'http://{host}:{port}/{path}'
    logger.info(f'getting data from api: GET {url}')
    result = get(url)
    return result
