import pytest

import brain.client

from brain.client import upload_sample

records_in_sample = 10


class MockAgent:
    instance = None  # implementing "weak" singleton

    def __init__(self, host, port):
        MockAgent.instance = self
        self.num_snapshots = 0

    def send_snapshot(self, snapshot):
        self.num_snapshots += 1


@pytest.fixture
def mock_agent(monkeypatch):
    monkeypatch.setattr(brain.client.client, 'get_server_agent', MockAgent)


@pytest.fixture(scope='module')
def sample_path(resources_path):
    return resources_path / 'tests_sample.mind.gz'


def test_upload_sample(mock_agent, sample_path):
    upload_sample('127.0.0.1', 1234, str(sample_path))
    assert MockAgent.instance is not None, 'Missing usage in agent'
    assert MockAgent.instance.num_snapshots == records_in_sample, 'Unexpected number of calls to send_snapshot'
