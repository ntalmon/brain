import functools
import logging
import pathlib
import sys

from brain import log_path
from brain.utils.config import client_config

fmt = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(level=logging.INFO, filename=str(log_path), format=fmt, datefmt=datefmt)


def get_logger(name):
    return logging.getLogger(name)


def normalize_path(path):
    return pathlib.Path(str(path))


def cli_suppress(f, logger=None):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as error:
            logger and logger.error(f'error while running command: {error}')
            if client_config['debug']:
                raise
            logger and logger.info(f'exiting program: code=1')
            sys.exit(1)

    return wrapper
