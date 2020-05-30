"""
The server module contains the main logic of the server, which is, receive incoming snapshots, construct message
to the parsers, and send them via the MQ.
"""

import threading

from brain.utils.common import get_logger, get_url_scheme
from .client_agent import load_client_agent
from .mq_agent import load_mq_agent
from .parsers_agent import construct_parsers_message
from ..autogen import client_server_pb2
from ..utils.consts import config

logger = get_logger(__name__)


def construct_publish(mq_url: str) -> callable:
    """
    Construct a `publish` function that publishes a given snapshot to the MQ.

    :param mq_url: address of the MQ.
    :return: the publish function.
    """

    logger.info(f'constructing publish function: {mq_url=}')
    mq_type = get_url_scheme(mq_url)
    mq_agent_module = load_mq_agent(mq_type)
    mq_agent = mq_agent_module.MQAgent(mq_url)

    def _publish(snapshot):
        mq_agent.publish_snapshot(snapshot)

    return _publish


snapshot_lock = threading.Lock()
snapshot_counter = 0


def generate_snapshot_uuid():
    # take a lock and increase the number of snapshots
    global snapshot_counter
    with snapshot_lock:
        uuid = snapshot_counter
        snapshot_counter += 1
    return uuid


def handle_snapshot(snapshot: client_server_pb2.Snapshot, publish: callable):
    """
    Handle an incoming snapshot: sends is to the provided publish function.

    :param snapshot: the snapshot object, in client_server_pb2.Snapshot format.
    :param publish: publish function, will be sent by client agent.
    """

    snapshot_uuid = generate_snapshot_uuid()
    logger.info(f'handling new snapshot, user_id={snapshot.user.user_id}, {snapshot_uuid=}')
    parsers_msg = construct_parsers_message(snapshot, snapshot_uuid)
    logger.debug(f'publishing snapshot to rabbitmq')
    publish(parsers_msg)  # publish the message with the given publish function


def run_server(host: str, port: int, publish: callable):
    """
    Run the server with a given publish function.

    :param host: server hostname.
    :param port: server port number.
    :param publish: publish function.
    """

    logger.info(f'running server: {host=}, {port=}, {publish=}')
    protocol = config['client_server_protocol']
    client_agent_module = load_client_agent(protocol)
    client_agent = client_agent_module.ClientAgent(publish=publish)
    client_agent.register_snapshot_handler(handle_snapshot)
    client_agent.run(host, port)
