import multiprocessing

import pytest
import brain.server.client_agent

from brain.server import run_server

HOST = 'localhost'
PORT = 8000


@pytest.fixture
def run_server_in_background():
    parent, child = multiprocessing.Pipe()

    def _run_server():
        run_server(HOST, PORT, None)

    process = multiprocessing.Process(target=_run_server)
    process.start()
    parent.recv()
    try:
        yield lambda: parent.recv()
    finally:
        process.terminate()
        process.join()


class MockFlask:
    class Request:
        method = None
        data = None

    request = Request
    app = None

    class Flask:
        def __init__(self, name):
            MockFlask.app = self
            self.routes = {}

        def route(self, route, methods=None):
            if not methods:
                methods = ['GET']

            def decorator(f):
                def wrapper(*args, **kwargs):
                    return f(*args, **kwargs)

                return wrapper

            return decorator

        def run(self):
            pass

    @classmethod
    def send_request(cls):
        pass


@pytest.fixture
def mock_flask(monkeypatch):
    monkeypatch.setattr(brain.server.client_agent, 'flask', MockFlask)


def test_server():
    assert False
