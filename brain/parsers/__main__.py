import json

import click

from brain.utils.common import cli_suppress, get_logger
from . import run_parser, invoke_parser

logger = get_logger(__name__)


@click.group()
def cli():
    pass


@cli.command('parse')
@click.argument('parser', type=click.STRING)
@click.argument('path', type=click.STRING)
@cli_suppress
def cli_parse(parser: str, path: str):
    """
    Run the given parser with the data in the given path, and print the result.
    """

    logger.info(f'running cli parse: {parser=}, {path=}')
    result = run_parser(parser, path, is_path=True)
    result = json.dumps(result)
    print(result)


@cli.command('run-parser')
@click.argument('parser', type=click.STRING)
@click.argument('mq', type=click.STRING)
@cli_suppress
def cli_run_parser(parser: str, mq: str):
    """
    Run the parser as a service, that consumes messages and publishes results using the given MQ.
    """

    logger.info(f'running cli run-parser: {parser=}, {mq=}')
    invoke_parser(parser, mq)


if __name__ == '__main__':
    cli(prog_name='parsers')
