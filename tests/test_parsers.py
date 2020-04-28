import os

import pytest

import brain.parsers
from brain.parsers import run_parser, invoke_parser
from tests.data_generators import gen_server_snapshot
from tests.utils import protobuf2dict

mq_url = 'rabbitmq://127.0.0.1:5672'


@pytest.fixture
def parsers_snapshot(tmp_path):
    snapshot = gen_server_snapshot(tmp_path)
    data = snapshot.SerializeToString()
    return snapshot, data


def verify_result_header(result, snapshot):
    assert result['uuid'] == str(snapshot.uuid)  # TODO: this is workaround, solve the problem
    assert result['datetime'] == str(snapshot.datetime)
    assert result['user'] == protobuf2dict(snapshot.user)


def test_pose(parsers_snapshot):
    snapshot, data = parsers_snapshot
    result = run_parser('pose', data)
    verify_result_header(result, snapshot)
    res = result['result']
    assert res == protobuf2dict(snapshot.pose)


def test_color_image(parsers_snapshot):
    snapshot, data = parsers_snapshot
    result = run_parser('color-image', data)
    verify_result_header(result, snapshot)
    res = result['result']
    assert os.path.isfile(res)


def test_depth_image(parsers_snapshot):
    snapshot, data = parsers_snapshot
    result = run_parser('depth-image', data)
    verify_result_header(result, snapshot)
    res = result['result']
    assert os.path.isfile(res)


def test_feelings(parsers_snapshot):
    snapshot, data = parsers_snapshot
    result = run_parser('feelings', data)
    verify_result_header(result, snapshot)
    res = result['result']
    assert res == protobuf2dict(snapshot.feelings)


class MockMQAgent:
    def __init__(self, url):
        pass

    def consume_snapshots(self, callback, topic):
        pass

    def publish_result(self, result, topic):
        pass

    @classmethod
    def clear(cls):
        pass


@pytest.fixture
def mock_mq_agent(monkeypatch):
    yield monkeypatch.setattr(brain.parsers.parsers, 'MQAgent', MockMQAgent)
    MockMQAgent.clear()


def test_invoke_parser(mock_mq_agent):
    invoke_parser('pose', 'rabbitmq://127.0.0.1:5672')
    assert False


def test_mq_agent():
    assert False


def test_cli():
    assert False
