import flask

from brain.autogen import client_server_pb2
from brain.utils.common import get_logger

logger = get_logger(__name__)
app = flask.Flask(__name__)
snapshot_handlers = []


def snapshot_handler(f):
    logger.info(f'detected new snapshot handler: {f=}')
    snapshot_handlers.append(f)


@app.route('/snapshot', methods=['POST'])
def handle_snapshot():
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


def run(host, port):
    logger.info(f'starting to run flask app: {host=}, {port=}')
    app.run(host=host, port=port)
