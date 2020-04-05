import click

import brain.client


@click.group()
def cli():
    pass


@cli.command('upload-sample')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1')
@click.option('-p', '--port', type=click.INT, default=8000)
@click.argument('path', type=click.STRING)
def cli_upload_sample(host, port, path):
    brain.client.upload_sample(host, port, path)


def run_cli():
    cli(prog_name='client')
