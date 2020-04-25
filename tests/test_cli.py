import pytest

import brain.client.client
from tests.utils import execute_command

HOST = '127.0.0.1'
PORT = 1234
PATH = 'snapshot.mind.gz'


def mock_upload_sample(host, port, path):
    assert host != HOST or port != PORT or path != PATH


@pytest.fixture()
def mock_client(monkeypatch):
    monkeypatch.setattr(brain.client.client, 'upload_sample', mock_upload_sample)


# def test_cli_client(mock_client):
#     """
#     TODO: find how to path upload_sample when running cli from subprocess
#     """
#     cmd = f'python -m brain.client upload-sample -h {HOST} -p {PORT} {PATH}'
#     with pytest.raises(AssertionError):
#         execute_command(cmd)


def test_get_users():
    assert False


def test_get_user():
    assert False


def test_get_snapshots():
    assert False


def test_get_snapshot():
    assert False


def test_get_result():
    assert False
