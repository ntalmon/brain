import click

from brain.utils.common import cli_suppress, get_logger
from brain.utils.consts import *
from .api_agent import api_get

logger = get_logger(__name__)


@click.group()
@click.option('-h', '--host', type=click.STRING, default=API_HOST, help='API server hostname.')
@click.option('-p', '--port', type=click.INT, default=API_PORT, help='API server port number.')
@click.pass_context
@cli_suppress
def cli(ctx, host, port):
    """
    All the commands have the `-h/--host` and `-p/--port` flags which refer to the API address
    """

    # pass host and port to all cli commands.
    ctx.ensure_object(dict)
    ctx.obj['host'] = host
    ctx.obj['port'] = port


@cli.command('get-users')
@click.pass_context
@cli_suppress
def cli_get_users(ctx):
    """
    Get all supported users.
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
    Get user details.
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
    Get user snapshots.
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
def cli_get_snapshot(ctx, user_id: int, snapshot_id: int):
    """
    Get snapshot details.
    """

    host, port = ctx.obj['host'], ctx.obj['port']
    logger.info(f'running cli get-snapshot: {host=}, {port=}, {user_id=}, {snapshot_id=}')
    result = api_get(host, port, f'users/{user_id}/snapshots/{snapshot_id}')
    print(result)


@cli.command('get-result')
@click.option('-s', '--save', type=click.STRING, help="If given, save the result to the given path.")
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
@click.argument('result_name', type=click.STRING)
@click.pass_context
@cli_suppress
def cli_get_result(ctx, save, user_id, snapshot_id, result_name):
    """
    Get parsing result of a snapshot.
    """

    host, port = ctx.obj['host'], ctx.obj['port']
    logger.info(f'running cli get-result: {host=}, {port=}, {user_id=}, {snapshot_id=}, {result_name=}')
    result = api_get(host, port, f'users/{user_id}/snapshots/{snapshot_id}/{result_name}')

    if save:
        with open(save, 'w') as file:
            file.write(result)
    else:
        print(result)


if __name__ == '__main__':
    cli(prog_name='cli')
