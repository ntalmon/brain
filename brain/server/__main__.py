import click

from brain.server import run_server, construct_publish
from brain.utils.common import cli_main


@click.group()
def cli():
    pass


# TODO: update defaults
@cli.command('run-server')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1')
@click.option('-p', '--port', type=click.INT, default=8000)
@click.argument('mq', type=click.STRING)
def cli_run_server(host, port, mq):
    """
    TODO: handle publish argument
    """
    publish = construct_publish(mq)
    run_server(host, port, publish)


if __name__ == '__main__':
    cli_main(cli, prog_name='server')
