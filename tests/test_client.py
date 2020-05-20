import pytest
from click.testing import CliRunner

import brain.client.server_agent

from brain.autogen import protocol_pb2
from brain.client import upload_sample
from brain.client.__main__ import cli
from .consts import *


@pytest.fixture
def mock_server(monkeypatch):
    calls = []

    def mock_post(url, data):
        calls.append((url, data))
        return 200

    monkeypatch.setattr(brain.client.server_agent, 'post', mock_post)
    return calls


def test_client(random_sample, mock_server):
    user, snapshots, file_path = random_sample
    upload_sample(SERVER_HOST, SERVER_PORT, file_path)
    calls = mock_server
    assert len(calls) == len(snapshots)
    for call, snapshot in zip(calls, snapshots):
        url, data = call
        result = protocol_pb2.Snapshot()
        result.ParseFromString(data)
        assert result.datetime == snapshot.datetime
        assert str(result.user) == str(user)
        assert str(result.pose) == str(snapshot.pose)
        assert str(result.color_image) == str(snapshot.color_image)
        assert str(result.depth_image) == str(snapshot.depth_image)
        assert str(result.feelings) == str(snapshot.feelings)


def test_cli(resources_path, mock_server):
    sample_path = resources_path / 'tests_sample.mind.gz'
    runner = CliRunner()
    result = runner.invoke(cli, ['upload-sample', str(sample_path)])
    assert result.exit_code == 0
    assert 'All snapshots uploaded successfully' in result.output
