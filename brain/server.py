from flask import Flask

app = Flask(__name__)


@app.route('/config')
def config():
    pass


@app.route('/snapshot')
def snapshot():
    pass


def run_server(host, port, publish):
    """
    TODO: handle publish
    """
    app.run(host=host, port=port)


if __name__ == '__main__':
    from brain.cli.server import run_cli

    run_cli()
