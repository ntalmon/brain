import requests

from brain.utils.common import get_logger

logger = get_logger(__name__)


def get(url, expect=200):
    logger.debug(f'GET request: {url=}, {expect=}')
    response = requests.get(url)
    if expect and response.status_code != expect:
        logger.error(f'GET {url} failed with exit-code {response.status_code}')
        raise Exception(f'GET {url} failed with exit-code {response.status_code}')
    return response.text


def post(url, data, expect=200):
    logger.debug(f'POST request: {url=}, {expect=}')
    response = requests.post(url, data)
    if expect and response.status_code != expect:
        logger.error(f'POST {url} failed with exit-code {response.status_code}')
        raise Exception(f'POST {url} failed with exit-code {response.status_code}')
    return response.text
