import multiprocessing
import threading
from functools import partial

import pytest

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


def test_server():
    assert False
