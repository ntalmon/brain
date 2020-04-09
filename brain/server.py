from brain.protocol import HTTPAgent

agent = HTTPAgent()  # TODO: auto find the right agent according to configuration


@agent.config_handler
def handle_config():
    pass


@agent.snapshot_handler
def handle_snapshot(snapshot):
    """
    TODO: move to protocol format
    """
    snapshot_msg = snapshot.SerializeToString()
    agent.publish(snapshot_msg)


def run_server(host, port, publish):
    """
    TODO: handle publish
    """
    agent.publish = publish
    agent.run(host, port)


if __name__ == '__main__':
    from brain.cli.server import run_cli

    run_cli()
