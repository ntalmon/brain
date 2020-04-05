import click


@click.group()
def cli():
    pass


@cli.command('upload-sample')
@click.argument('host')
@click.argument('port')
@click.argument('path')
def cli_upload_sample(host, port, path):
    import brain.client
    brain.client.upload_thought(host, port, path)


def run_cli():
    cli(prog_name='client')
