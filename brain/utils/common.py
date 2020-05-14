import sys

from brain.utils.config import client_config


def cli_main(callback, *args, **kwargs):
    try:
        callback(*args, **kwargs)
    except Exception as error:
        if client_config['debug']:
            raise
        print(f'ERROR: {error}')
        sys.exit(1)
