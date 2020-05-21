import click

from brain.utils.common import cli_suppress
from brain.utils.consts import *
from .client import upload_sample


@click.group()
def cli():
    pass


@cli.command('upload-sample')
@click.option('-h', '--host', type=click.STRING, default=SERVER_HOST)
@click.option('-p', '--port', type=click.INT, default=SERVER_PORT)
@click.argument('path', type=click.STRING)
@cli_suppress
def cli_upload_sample(host, port, path):
    upload_sample(host, port, path)


if __name__ == '__main__':
    cli(prog_name='client')
