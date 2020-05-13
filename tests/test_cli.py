import pytest

import brain.client.client

HOST = '127.0.0.1'
PORT = 1234
PATH = 'snapshot.mind.gz'


def mock_upload_sample(host, port, path):
    assert host != HOST or port != PORT or path != PATH


@pytest.fixture()
def mock_client(monkeypatch):
    monkeypatch.setattr(brain.client.client, 'upload_sample', mock_upload_sample)


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
