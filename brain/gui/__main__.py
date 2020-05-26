import click

from brain.utils.common import cli_suppress, get_logger
from brain.utils.consts import *
from . import run_server

logger = get_logger(__name__)


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', type=click.STRING, default=GUI_HOST)
@click.option('-p', '--port', type=click.INT, default=GUI_PORT)
@click.option('-H', '--api-host', type=click.STRING, default=API_HOST)
@click.option('-P', '--api-port', type=click.INT, default=API_PORT)
@cli_suppress
def cli_run_server(host, port, api_host, api_port):
    logger.info(f'running cli run-server: {host=}, {port=}, {api_host=}, {api_port=}')
    run_server(host, port, api_host, api_port)


if __name__ == '__main__':
    cli(prog_name='gui')
