import threading
from functools import partial

from brain import server

HOST = 'localhost'
PORT = 8000


def publish(message):
    print(message)


def test_run_server(capsys):
    _run_server = partial(server.run_server, HOST, PORT, publish)
    thread = threading.Thread(target=_run_server)
    thread.start()
