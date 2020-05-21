import click

from brain.utils.common import cli_suppress
from brain.utils.consts import *
from . import run_saver, Saver


@click.group()
def cli():
    pass


@cli.command('save')
@click.option('-d', '--database', type=click.STRING, default=DB_URL)
@click.argument('topic', type=click.STRING)
@click.argument('path', type=click.STRING)
@cli_suppress
def cli_save(database, topic, path):
    saver = Saver(database)
    with open(path, 'r') as file:  # TODO: handle errors
        data = file.read()
        saver.save(topic, data)


@cli.command('run-saver')
@click.argument('database', type=click.STRING)
@click.argument('mq', type=click.STRING)
@cli_suppress
def cli_run_saver(database, mq):
    run_saver(database, mq)


if __name__ == '__main__':
    cli(prog_name='saver')
