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
    brain.parsers.run_parser(parser, path)


@cli.command('run-parser')
@click.argument('parser', type=click.STRING)
@click.argument('mq', type=click.STRING)
def cli_run_parser(parser, mq):
    brain.parsers.invoke_parser(parser, mq)


def run_cli():
    cli(prog_name='parsers')
