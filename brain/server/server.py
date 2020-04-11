from brain.mq import MQAgent
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
    mq_agent = MQAgent(mq_url)

    def publish(snapshot):
        mq_agent.publish(snapshot, exchange='snapshot')

    return publish


@client_agent.snapshot_handler
def handle_snapshot(snapshot):
    parsers_msg = construct_parsers_message(snapshot)
    client_agent.publish(parsers_msg)


def run_server(host, port, publish):
    """
    TODO: handle publish
    """
    client_agent.publish = publish
    client_agent.run(host, port)
