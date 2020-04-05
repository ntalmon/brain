import click


@click.group()
def cli():
    pass


@cli.command('parse')
def cli_parse():
    pass


@cli.command('run-parser')
def cli_run_parser():
    pass


def run_cli():
    cli(prog_name='parsers')
