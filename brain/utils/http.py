"""
The HTTP module provides interface for HTTP requests, and return-code handling.
"""

import requests

from brain.utils.common import get_logger

logger = get_logger(__name__)


def get(url: str, expect: int = 200) -> str:
    """
    Execute GET request, and check for expected return-code.

    :param url: request this url.
    :param expect: expected return-code. An exception will be raised if different code was returned.
    :return: response text.
    """

    logger.debug(f'GET request: {url=}, {expect=}')
    response = requests.get(url)
    if expect and response.status_code != expect:
        logger.error(f'GET {url} failed with exit-code {response.status_code}')
        raise Exception(f'GET {url} failed with exit-code {response.status_code}')
    return response.text


def post(url, data, expect=200):
    """
    Execute POST request, and check for expected return-code.

    :param url: request this url.
    :param data:  data to send with the POST request.
    :param expect: expected return-code. An exception will be raised if different code was returned.
    :return: the response text.
    """

    logger.debug(f'POST request: {url=}, {expect=}')
    response = requests.post(url, data)
    if expect and response.status_code != expect:
        logger.error(f'POST {url} failed with exit-code {response.status_code}')
        raise Exception(f'POST {url} failed with exit-code {response.status_code}')
    return response.text
