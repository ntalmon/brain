import pytest

import brain.parsers
from brain.parsers import run_parser, invoke_parser

mq_url = 'rabbitmq://127.0.0.1:5672'


@pytest.fixture
def snapshot_example(snapshot_generator):  # TODO: change this
    return next(snapshot_generator(1))


def test_pose(snapshot_example):
    result = run_parser('pose', snapshot_example)
    assert False


def test_color_image(snapshot_example):
    result = run_parser('color-image', snapshot_example)
    assert False


def test_depth_image(snapshot_example):
    result = run_parser('depth-image', snapshot_example)
    assert False


def test_feelings():
    result = run_parser('feelings', snapshot_example)
    assert False


class MockMQAgent:
    def __init__(self, url):
        pass

    def consume_snapshots(self, callback, topic):
        pass

    def publish_result(self, result, topic):
        pass


@pytest.fixture
def mock_mq_agent(monkeypatch):
    monkeypatch.setattr(brain.parsers.parsers, 'MQAgent', MockMQAgent)


def test_invoke_parser(mock_mq_agent):
    invoke_parser('pose', 'rabbitmq://127.0.0.1:5672')
    assert False


def test_mq_agent():
    assert False


def test_cli():
    assert False
