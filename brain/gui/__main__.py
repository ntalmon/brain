import sys

from brain.utils.config import client_config

if __name__ == '__main__':
    from brain.cli.gui import run_cli

    try:
        run_cli()
    except Exception as error:
        if client_config['debug']:
            raise
        print(f'ERROR: {error}')
        sys.exit(1)
