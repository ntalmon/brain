import click

from brain.utils.common import cli_suppress, get_logger
from brain.utils.consts import *
from . import run_server, construct_publish

logger = get_logger(__name__)


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', type=click.STRING, default=SERVER_HOST, help='Server hostname.')
@click.option('-p', '--port', type=click.INT, default=SERVER_PORT, help='Server port number.')
@click.argument('mq', type=click.STRING)
@cli_suppress
def cli_run_server(host: str, port: int, mq: str):
    """
    Run the server.
    """

    logger.info(f'running cli run-server: {host=}, {port=}, {mq=}')
    publish = construct_publish(mq)
    run_server(host, port, publish)


if __name__ == '__main__':
    cli(prog_name='server')
