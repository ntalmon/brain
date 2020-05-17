import threading

from .client_agent import snapshot_handler, run
from .mq_agent import MQAgent
from .parsers_agent import construct_parsers_message

publish_fn = None


def construct_publish(mq_url):
    mq_agent = MQAgent(mq_url)

    def _publish(snapshot):
        mq_agent.publish_snapshot(snapshot)

    return _publish


snapshot_lock = threading.Lock()
snapshot_counter = 0


def generate_snapshot_uuid():  # TODO: is this the right way to generate uuid?
    global snapshot_counter
    with snapshot_lock:
        uuid = snapshot_counter
        snapshot_counter += 1
    return uuid


@snapshot_handler
def handle_snapshot(snapshot):
    snapshot_uuid = generate_snapshot_uuid()
    parsers_msg = construct_parsers_message(snapshot, snapshot_uuid)
    publish_fn(parsers_msg)


def init_publish(publish):
    global publish_fn
    publish_fn = publish


def run_server(host, port, publish):
    init_publish(publish)
    run(host, port)
