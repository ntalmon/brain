"""
The client agent provides an interface for the server to accept connection and receive snapshots from clients.
It runs as a server that receives messages, parses them and then passes them to the server (brain.server.server)
by calling registered handlers.
"""

import flask

from brain.autogen import client_server_pb2
from brain.utils.common import get_logger

logger = get_logger(__name__)
app = flask.Flask(__name__)
snapshot_handlers = []


def snapshot_handler(f: callable):
    """
    The snapshot_handler decorator gets a callback, and whenever a snapshot is received, the callback will be called
    with the parsed snapshot.

    :param f: the callback function
    """

    logger.info(f'detected new snapshot handler: {f=}')
    snapshot_handlers.append(f)


@app.route('/snapshot', methods=['POST'])
def handle_snapshot():
    """
    Handle incoming snapshot. Parse the snapshot (to client_server_pb2.Snapshot format) and call registered handlers
    with the parsed snapshot.
    """

    logger.debug(f'received new snapshot message')
    snapshot_msg = flask.request.data
    snapshot = client_server_pb2.Snapshot()
    try:
        snapshot.ParseFromString(snapshot_msg)
    except Exception as error:
        logger.error(f'error while parsing message: {error}. aborting (404)')
        flask.abort(400)
    for handler in snapshot_handlers:
        handler(snapshot)
    return 'Snapshot handled successfully'


def run(host: str, port: int):
    """
    Run the listening server, i.e. the flask app.

    :param host: hostname to listen.
    :param port: port number to listen.
    """

    logger.info(f'starting to run flask app: {host=}, {port=}')
    app.run(host=host, port=port)
