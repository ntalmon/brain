import click

from brain.utils.common import cli_suppress, get_logger
from brain.utils.consts import *
from .client import upload_sample

logger = get_logger(__name__)


@click.group()
def cli():
    pass


@cli.command('upload-sample')
@click.option('-h', '--host', type=click.STRING, default=SERVER_HOST, help='Server hostname.')
@click.option('-p', '--port', type=click.INT, default=SERVER_PORT, help='Server port number.')
@click.argument('path', type=click.STRING)
@cli_suppress
def cli_upload_sample(host, port, path):
    """
    Reads the sample file and stream the snapshots to the server.
    """

    logger.info(f'running cli upload-sample: {host=}, {port=}, {path=}')
    count = upload_sample(host, port, path)
    print(f'Successfully uploaded {count} snapshots')


if __name__ == '__main__':
    cli(prog_name='client')
