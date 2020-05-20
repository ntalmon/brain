import flask

from brain.autogen import client_server_pb2

app = flask.Flask(__name__)
snapshot_handlers = []


def snapshot_handler(f):
    snapshot_handlers.append(f)


@app.route('/snapshot', methods=['POST'])
def handle_snapshot():
    snapshot_msg = flask.request.data
    snapshot = client_server_pb2.Snapshot()
    try:
        snapshot.ParseFromString(snapshot_msg)
    except Exception as error:
        print(error)
        flask.abort(400)
    for handler in snapshot_handlers:
        handler(snapshot)
    return 'Snapshot handled successfully'


def run(host, port):
    app.run(host=host, port=port)
