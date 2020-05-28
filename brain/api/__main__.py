import click

from brain.utils.common import cli_suppress, get_logger
from brain.utils.consts import *
from . import run_api_server

logger = get_logger(__name__)


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', type=click.STRING, default=API_HOST, help='server hostname')
@click.option('-p', '--port', type=click.INT, default=API_PORT, help='server port number')
@click.option('-d', '--database', type=click.STRING, default=MQ_URL, help='database address to fetch results from')
@cli_suppress
def cli_run_server(host, port, database):
    """
    Run the api server.
    """

    logger.info(f'running cli run-server: {host=}, {port=}, {database=}')
    run_api_server(host, port, database)


if __name__ == '__main__':
    cli(prog_name='api')
