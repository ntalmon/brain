import click

from brain.utils.common import cli_suppress, get_logger
from brain.utils.consts import *
from . import run_api_server

logger = get_logger(__name__)


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', type=click.STRING, default=API_HOST)
@click.option('-p', '--port', type=click.INT, default=API_PORT)
@click.option('-d', '--database', type=click.STRING, default=MQ_URL)
@cli_suppress
def cli_run_server(host, port, database):
    logger.info(f'running cli run-server: {host=}, {port=}, {database=}')
    run_api_server(host, port, database)


if __name__ == '__main__':
    cli(prog_name='api')
