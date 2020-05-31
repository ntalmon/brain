"""
The HTTP client agent module provides a client agent of http protocol.
"""

import flask

from brain.autogen import client_server_pb2
from brain.server.client_agent.base_client_agent import BaseClientAgent
from brain.utils.common import get_logger, parse_protobuf

logger = get_logger(__name__)


class ClientAgent(BaseClientAgent):
    """
    HTTP-based implementation of client agent.
    """

    def __init__(self, publish: callable = None):
        BaseClientAgent.__init__(self, publish=publish)
        self.app = flask.Flask(__name__)  # use flask for the server
        self.snapshot_handlers = []

        @self.app.route('/snapshot', methods=['POST'])
        def handle_snapshot():
            # pass to instance method.
            return self.handle_snapshot()

    def register_snapshot_handler(self, handler: callable):
        logger.info(f'detected new snapshot handler: {handler=}')
        self.snapshot_handlers.append(handler)  # add snapshot handler

    def handle_snapshot(self):
        logger.debug(f'received new snapshot message')
        snapshot_msg = flask.request.data

        try:
            # parse snapshot
            snapshot = parse_protobuf(client_server_pb2.Snapshot(), snapshot_msg)
        except Exception as error:
            logger.error(f'error while parsing message: {error}. aborting (404)')
            return flask.abort(400)

        # calling the registered handlers
        for handler in self.snapshot_handlers:
            handler(snapshot, self.publish)

        return 'Snapshot handled successfully'

    def run(self, host: str, port: int):
        logger.info(f'starting to run flask app: {host=}, {port=}')
        self.app.run(host=host, port=port)  # simply run the flask app
