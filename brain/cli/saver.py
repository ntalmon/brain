import click

from brain.saver import Saver, run_saver


@click.group()
def cli():
    pass


# TODO: update defaults
@cli.command('save')
@click.option('-d', '--database', type=click.STRING, default='postgresql://127.0.0.1:5432')
@click.argument('topic', type=click.STRING)
@click.argument('path', type=click.STRING)
def cli_save(database, topic, path):
    saver = Saver(database)
    with open(path, 'r') as file:  # TODO: handle errors
        data = file.read()
        saver.save(topic, data)


@cli.command('run-saver')
@click.argument('db_url', type=click.STRING)
@click.argument('mq_url', type=click.STRING)
def cli_run_saver(db_url, mq_url):
    run_saver(db_url, mq_url)


def run_cli():
    cli(prog_name='saver')
