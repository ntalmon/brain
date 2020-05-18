import click

from .api_agent import api_get
from brain.utils.common import cli_suppress


@click.group()
@click.option('-h', '--host', type=click.STRING, default='127.0.0.1')
@click.option('-p', '--port', type=click.INT, default=5000)
@click.pass_context
@cli_suppress
def cli(ctx, host, port):
    ctx.ensure_object(dict)
    ctx.obj['host'] = host
    ctx.obj['port'] = port


@cli.command('get-users')
@click.pass_context
@cli_suppress
def get_users(ctx):
    host, port = ctx.obj['host'], ctx.obj['port']
    result = api_get(host, port, 'users')
    print(result)


@cli.command('get-user')
@click.argument('user_id', type=click.INT)
@click.pass_context
@cli_suppress
def cli_get_users(ctx, user_id):
    host, port = ctx.obj['host'], ctx.obj['port']
    result = api_get(host, port, f'users/{user_id}')
    print(result)


@cli.command('get-snapshots')
@click.argument('user_id', type=click.INT)
@click.pass_context
@cli_suppress
def cli_get_snapshots(ctx, user_id):
    host, port = ctx.obj['host'], ctx.obj['port']
    result = api_get(host, port, f'users/{user_id}/snapshots')
    print(result)


@cli.command('get-snapshot')
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
@click.pass_context
@cli_suppress
def cli_get_snapshot(ctx, user_id, snapshot_id):
    host, port = ctx.obj['host'], ctx.obj['port']
    result = api_get(host, port, f'users/{user_id}/snapshots/{snapshot_id}')
    print(result)


@cli.command('get-result')
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
@click.argument('result_name', type=click.STRING)
@click.pass_context
@cli_suppress
def cli_get_result(ctx, user_id, snapshot_id, result_name):
    host, port = ctx.obj['host'], ctx.obj['port']
    result = api_get(host, port, f'users/{user_id}/snapshots/{snapshot_id}/{result_name}')
    print(result)


if __name__ == '__main__':
    cli(prog_name='cli')
