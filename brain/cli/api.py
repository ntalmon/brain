import click

from brain.api.api import run_api_server


@click.group()
def cli():
    pass


# TODO: update defaults
@cli.command('run-server')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1')
@click.option('-p', '--port', type=click.INT, default=5000)
@click.option('-d', '--database', type=click.STRING, default='mongodb://127.0.0.1:27017')
def cli_run_server(host, port, database):
    run_api_server(host, port, database)


def run_cli():
    cli(prog_name='api')
