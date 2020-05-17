import click

from . import upload_sample
from brain.utils.common import cli_suppress


@click.group()
def cli():
    pass


@cli.command('upload-sample')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1')
@click.option('-p', '--port', type=click.INT, default=8000)
@click.argument('path', type=click.STRING)
@cli_suppress
def cli_upload_sample(host, port, path):
    upload_sample(host, port, path)


if __name__ == '__main__':
    cli(prog_name='client')
