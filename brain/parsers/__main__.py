import click

from brain.utils.common import cli_suppress
from . import run_parser, invoke_parser


@click.group()
def cli():
    pass


@cli.command('parse')
@click.argument('parser', type=click.STRING)
@click.argument('path', type=click.STRING)
@cli_suppress
def cli_parse(parser, path):
    import json
    result = run_parser(parser, path, is_path=True)
    result = json.dumps(result)
    print(result)


@cli.command('run-parser')
@click.argument('parser', type=click.STRING)
@click.argument('mq', type=click.STRING)
@cli_suppress
def cli_run_parser(parser, mq):
    invoke_parser(parser, mq)


if __name__ == '__main__':
    cli(prog_name='parsers')
