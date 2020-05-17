import click

from . import run_api_server
from brain.utils.common import cli_suppress


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1')
@click.option('-p', '--port', type=click.INT, default=5000)
@click.option('-d', '--database', type=click.STRING, default='mongodb://127.0.0.1:27017')
@cli_suppress
def cli_run_server(host, port, database):
    run_api_server(host, port, database)


if __name__ == '__main__':
    cli(prog_name='api')
