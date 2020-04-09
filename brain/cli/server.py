import click

import brain.server
from brain.mq import MQAgent


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1')
@click.option('-p', '--port', type=click.INT, default=8000)
@click.argument('url', type=click.STRING)
def cli_run_server(host, port, url):
    """
    TODO: handle publish argument
    """
    agent = MQAgent(url)

    def publish(snapshot):
        agent.publish(snapshot, exchange='snapshot')

    brain.server.run_server(host, port, publish)


def run_cli():
    cli(prog_name='server')
