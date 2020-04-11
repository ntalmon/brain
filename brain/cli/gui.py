import click


@click.group()
def cli():
    pass


# TODO: update defaults
@cli.command('run-server')
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1')
@click.option('-p', '--port', type=click.INT, default=8000)
@click.option('-d', '--database', type=click.STRING)  # TODO: default should be as API's default
def cli_run_server(host, port, database):
    pass


def run_cli():
    cli(prog_name='gui')
