import threading

from .mq_agent import get_mq_agent
from brain.server.client_agent import HTTPAgent
from brain.server.parsers_agent import construct_parsers_message

client_agents = {
    'http': HTTPAgent
}


def get_client_agent():
    protocol = 'http'  # TODO: extract from config
    if protocol not in client_agents:
        return None  # TODO: handle this case
    return client_agents[protocol]()


client_agent = get_client_agent()


def construct_publish(mq_url):
    mq_agent = get_mq_agent(mq_url)

    def publish(snapshot):
        mq_agent.publish_snapshot(snapshot)

    return publish


snapshot_lock = threading.Lock()
snapshot_counter = 0


def generate_snapshot_uuid():  # TODO: is this the right way to generate uuid?
    global snapshot_counter
    with snapshot_lock:
        uuid = snapshot_counter
        snapshot_counter += 1
    return uuid


@client_agent.snapshot_handler
def handle_snapshot(snapshot):
    snapshot_uuid = generate_snapshot_uuid()
    parsers_msg = construct_parsers_message(snapshot, snapshot_uuid)
    client_agent.publish(parsers_msg)


def run_server(host, port, publish):
    """
    TODO: handle publish
    """
    client_agent.publish = publish
    client_agent.run(host, port)
