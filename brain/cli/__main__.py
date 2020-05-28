import click

from brain.utils.common import cli_suppress, get_logger
from brain.utils.consts import *
from .api_agent import api_get

logger = get_logger(__name__)


@click.group()
@click.option('-h', '--host', type=click.STRING, default=API_HOST, help="API server hostname")
@click.option('-p', '--port', type=click.INT, default=API_PORT, help="API server port number")
@click.pass_context
@cli_suppress
def cli(ctx, host, port):
    # pass host and port to all cli commands.
    ctx.ensure_object(dict)
    ctx.obj['host'] = host
    ctx.obj['port'] = port


@cli.command('get-users')
@click.pass_context
@cli_suppress
def cli_get_users(ctx):
    """
    Get the list of all users.
    Retrieve result form DB and print.
    """
    host, port = ctx.obj['host'], ctx.obj['port']
    logger.info(f'running cli get-users: {host=}, {port=}')
    result = api_get(host, port, 'users')
    print(result)


@cli.command('get-user')
@click.argument('user_id', type=click.INT)
@click.pass_context
@cli_suppress
def cli_get_user(ctx, user_id):
    """
    Get a user by user id.
    Retrieve result form DB and print.

    :param: user_id: user id of the desired user
    """
    host, port = ctx.obj['host'], ctx.obj['port']
    logger.info(f'running cli get-user: {host=}, {port=}, {user_id=}')
    result = api_get(host, port, f'users/{user_id}')
    print(result)


@cli.command('get-snapshots')
@click.argument('user_id', type=click.INT)
@click.pass_context
@cli_suppress
def cli_get_snapshots(ctx, user_id):
    """
    Get a list of all snapshots related to a user, by user id.
    Retrieve result form DB and print.
    """
    host, port = ctx.obj['host'], ctx.obj['port']
    logger.info(f'running cli get-snapshots: {host=}, {port=}, {user_id=}')
    result = api_get(host, port, f'users/{user_id}/snapshots')
    print(result)


@cli.command('get-snapshot')
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
@click.pass_context
@cli_suppress
def cli_get_snapshot(ctx, user_id, snapshot_id):
    """
    Get a snapshot related to a user, by user id and snapshot id.
    Retrieve result form DB and print.
    """
    host, port = ctx.obj['host'], ctx.obj['port']
    logger.info(f'running cli get-snapshot: {host=}, {port=}, {user_id=}, {snapshot_id=}')
    result = api_get(host, port, f'users/{user_id}/snapshots/{snapshot_id}')
    print(result)


@cli.command('get-result')
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
@click.argument('result_name', type=click.STRING)
@click.pass_context
@cli_suppress
def cli_get_result(ctx, user_id, snapshot_id, result_name):
    """
    Get parsing result of a snapshot related to a user, by user id, snapshot id, and result name.
    Retrieve result form DB and print.
    """
    host, port = ctx.obj['host'], ctx.obj['port']
    logger.info(f'running cli get-result: {host=}, {port=}, {user_id=}, {snapshot_id=}, {result_name=}')
    result = api_get(host, port, f'users/{user_id}/snapshots/{snapshot_id}/{result_name}')
    print(result)


if __name__ == '__main__':
    cli(prog_name='cli')
