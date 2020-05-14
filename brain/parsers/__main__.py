import click

from brain.parsers import run_parser, invoke_parser
from brain.utils.common import cli_main


@click.group()
def cli():
    pass


@cli.command('parse')
@click.argument('parser', type=click.STRING)
@click.argument('path', type=click.STRING)
def cli_parse(parser, path):
    import json
    result = run_parser(parser, path, is_path=True)
    result = json.dumps(result)
    print(result)


@cli.command('run-parser')
@click.argument('parser', type=click.STRING)
@click.argument('mq', type=click.STRING)
def cli_run_parser(parser, mq):
    invoke_parser(parser, mq)


if __name__ == '__main__':
    cli_main(cli, prog_name='parsers')
