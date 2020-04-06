import click


@click.group()
def cli():
    pass


@cli.command('get-users')
def cli_get_users():
    pass


@cli.command('get-user')
@click.argument('user_id', type=click.INT)
def cli_get_users(user_id):
    pass


@cli.command('get-snapshots')
@click.argument('user_id', type=click.INT)
def cli_get_snapshots(user_id):
    pass


@cli.command('get-snapshot')
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
def cli_get_snapshot(user_id, snapshot_id):
    pass


@cli.command('get-result')
@click.argument('user_id', type=click.INT)
@click.argument('snapshot_id', type=click.INT)
def cli_get_result(user_id, snapshot_id):
    """
    TODO: complete this cli command arguments
    """
    pass


def run_cli():
    cli(prog_name='cli')
