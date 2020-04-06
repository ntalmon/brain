import click


@click.group()
def cli():
    pass


@cli.command('save')
@click.option('-d', '--database', type=click.STRING, default='postgresql://127.0.0.1:5432')  # TODO: update default
@click.argument('topic', type=click.STRING)
@click.argument('path', type=click.STRING)
def cli_save(database, topic, path):
    pass


@cli.command('run-saver')
@click.argument('saver', type=click.STRING)
@click.argument('mq', type=click.STRING)
def cli_run_saver(saver, mq):
    pass


def run_cli():
    cli(prog_name='saver')
