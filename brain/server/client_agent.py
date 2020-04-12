"""
TODO: separate between base agent and http agent
TODO: choose right agent according to url
TODO: remove config usage
TODO: make sure server is asynchronous and multithreaded
TODO: resolve flask-class issue
"""
import flask

from brain.autogen import protocol_pb2


class ClientAgent:
    config_handlers = []
    snapshot_handlers = []

    def __init__(self):
        self.publish = None

    @classmethod
    def config_handler(cls, f):
        cls.config_handlers.append(f)

    @classmethod
    def snapshot_handler(cls, f):
        cls.snapshot_handlers.append(f)

    def run(self, host, port):  # TODO: decide about 'publish'
        raise NotImplemented


class HTTPAgent(ClientAgent):
    app = flask.Flask(__name__)
    instance = None  # TODO: this about better design for it

    def __init__(self):
        ClientAgent.__init__(self)
        HTTPAgent.instance = self

    def send_config(self):
        for config_handler in self.config_handlers:
            config_handler()

    @staticmethod
    @app.route('/config')
    def _send_config():
        return HTTPAgent.instance.send_config()

    def get_snapshot(self):
        if flask.request.method == 'GET':
            return  # TODO: handle this case
        snapshot_msg = flask.request.data  # TODO: get exact post data
        snapshot = protocol_pb2.Snapshot()
        snapshot.ParseFromString(snapshot_msg)
        for snapshot_handler in self.snapshot_handlers:
            snapshot_handler(snapshot)
        return ''  # TODO: handle this

    @staticmethod
    @app.route('/snapshot', methods=['GET', 'POST'])
    def _get_snapshot():
        return HTTPAgent.instance.get_snapshot()

    def run(self, host, port):
        self.app.run(host, port)
