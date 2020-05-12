"""
TODO: separate between base agent and http agent
TODO: choose right agent according to url
TODO: remove config usage
TODO: make sure server is asynchronous and multithreaded
TODO: resolve flask-class issue
"""
import flask

from brain.autogen import protocol_pb2

app = flask.Flask(__name__)
snapshot_handlers = []


def snapshot_handler(f):
    snapshot_handlers.append(f)


@app.route('/snapshot', methods=['GET', 'POST'])
def handle_snapshot():
    if flask.request.method == 'GET':
        return  # TODO: handle this case
    snapshot_msg = flask.request.data  # TODO: get exact post data
    snapshot = protocol_pb2.Snapshot()
    snapshot.ParseFromString(snapshot_msg)
    for handler in snapshot_handlers:
        handler(snapshot)
    return ''  # TODO: handle this


def run(host, port):
    app.run(host=host, port=port)
