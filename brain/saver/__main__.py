import click

from brain.saver import run_saver, Saver
from brain.utils.common import cli_main


@click.group()
def cli():
    pass


@cli.command('save')
@click.option('-d', '--database', type=click.STRING, default='mongodb://127.0.0.1:27017')
@click.argument('topic', type=click.STRING)
@click.argument('path', type=click.STRING)
def cli_save(database, topic, path):
    saver = Saver(database)
    with open(path, 'r') as file:  # TODO: handle errors
        data = file.read()
        saver.save(topic, data)


@cli.command('run-saver')
@click.argument('database', type=click.STRING)
@click.argument('mq', type=click.STRING)
def cli_run_saver(database, mq):
    run_saver(database, mq)


if __name__ == '__main__':
    cli_main(cli, prog_name='saver')
