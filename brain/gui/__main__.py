import click

from brain.gui.gui import run_server
from brain.utils.common import cli_main


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1')
@click.option('-p', '--port', type=click.INT, default=8080)
@click.option('-H', '--api-host', type=click.STRING, default='127.0.0.1')
@click.option('-P', '--api-port', type=click.INT, default=5000)
def cli_run_server(host, port, api_host, api_port):
    run_server(host, port, api_host, api_port)


if __name__ == '__main__':
    cli_main(cli, prog_name='gui')
