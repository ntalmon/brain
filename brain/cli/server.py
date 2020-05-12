import click

import brain.server


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
    publish = brain.server.server.construct_publish(mq)
    brain.server.run_server(host, port, publish)


def run_cli():
    cli(prog_name='server')
