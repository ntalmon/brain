import click


@click.group()
def cli():
    pass


@cli.command('run-server')
@click.argument('host')
@click.argument('port')
@click.argument('publish')
def cli_run_server(host, port, publish):
    import brain.server
    brain.server.run_server(host, port, publish)


def run_cli():
    cli(prog_name='server')
