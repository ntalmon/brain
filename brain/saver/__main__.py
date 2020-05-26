import click

from brain.utils.common import cli_suppress, get_logger
from brain.utils.consts import *
from . import run_saver, Saver

logger = get_logger(__name__)


@click.group()
def cli():
    pass


@cli.command('save')
@click.option('-d', '--database', type=click.STRING, default=DB_URL)
@click.argument('topic', type=click.STRING)
@click.argument('path', type=click.STRING)
@cli_suppress
def cli_save(database, topic, path):
    logger.info(f'running cli save: {database=}, {topic=}, {path=}')
    saver = Saver(database)
    try:
        with open(path, 'r') as file:
            data = file.read()
    except OSError as error:
        logger.error(f'error while trying to read {path}: {error}')
        raise
    saver.save(topic, data)


@cli.command('run-saver')
@click.argument('database', type=click.STRING)
@click.argument('mq', type=click.STRING)
@cli_suppress
def cli_run_saver(database, mq):
    logger.info(f'running cli run-saver: {database=}, {mq=}')
    run_saver(database, mq)


if __name__ == '__main__':
    cli(prog_name='saver')
