import functools
import pathlib
import sys

from brain.utils.config import client_config


def normalize_path(path):
    return pathlib.Path(str(path))


def cli_suppress(f):
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as error:
            if client_config['debug']:
                raise
            print(f'ERROR: {error}')
            sys.exit(1)

    return wrapper
