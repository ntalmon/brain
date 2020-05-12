from functools import wraps

import click

from brain.utils.http import get


def api_get(host, port, path):
    url = f'http://{host}:{port}/{path}'
    result = get(url)
    return result


@click.group()
def cli():
    pass


def cli_base(command):
    def decorator(f):
        @cli.command(command)
        @click.option('-h', '--host', type=click.STRING, default='127.0.0.1')
        @click.option('-p', '--port', type=click.INT, default=5000)
        @wraps(f)
        def wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        return wrapper

    return decorator


@cli_base('get-users')
def get_users(host, port):
    res = api_get(host, port, 'users')
    print(res)


@cli_base('get-user')
@click.argument('user_id', type=click.INT)
def cli_get_users(host, port, user_id):
    print(host, port, user_id)


@cli_base('get-snapshots')
@click.argument('user_id', type=click.INT)
def cli_get_snapshots(user_id):
    pass


@cli_base('get-snapshot')
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
def cli_get_snapshot(user_id, snapshot_id):
    pass


@cli_base('get-result')
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
@click.argument('result_name', type=click.STRING)
def cli_get_result(user_id, snapshot_id, result_name):
    """
    TODO: complete this cli command arguments
    """
    pass


def run_cli():
    cli(prog_name='cli')
