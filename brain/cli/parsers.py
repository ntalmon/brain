import click

import brain.parsers


@click.group()
def cli():
    pass


@cli.command('parse')
@click.argument('parser', type=click.STRING)
@click.argument('path', type=click.STRING)
def cli_parse(parser, path):
    """
    TODO: handle path
    """
    brain.parsers.parse(parser, path)


@cli.command('run-parser')
@click.argument('parser', type=click.STRING)
@click.argument('url', type=click.STRING)
def cli_run_parser(parser, url):
    pass


def run_cli():
    cli(prog_name='parsers')
