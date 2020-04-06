import click


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1')
@click.option('-p', '--port', type=click.INT, default=5000)
@click.option('-d', '--database', type=click.STRING, default='postgresql://127.0.0.1')
def cli_save(host, port, database):
    pass


def run_cli():
    cli(prog_name='api')
