import json
import os

import pytest
from click.testing import CliRunner

import brain.parsers
import brain.parsers.mq_agent
from brain.autogen import server_parsers_pb2
from brain.parsers import run_parser, invoke_parser
from brain.parsers.__main__ import cli
from brain.parsers.mq_agent import MQAgent
from brain.utils.consts import *
from .data_generators import gen_snapshot
from .utils import protobuf2dict


@pytest.fixture
def random_snapshot(tmp_path):
    snapshot = gen_snapshot(server_parsers_pb2.Snapshot(), 'parser', tmp_path=tmp_path, should_gen_user=True)
    data = snapshot.SerializeToString()
    file_path = str(tmp_path / 'snapshot.raw')
    with open(file_path, 'wb') as file:
        file.write(data)
    return snapshot, data, file_path


def verify_result_header(result, snapshot):
    assert result['uuid'] == str(snapshot.uuid)  # TODO: this is workaround, solve the problem
    assert result['datetime'] == str(snapshot.datetime)
    assert result['user'] == protobuf2dict(snapshot.user)


def verify_pose(result, snapshot):
    assert result == protobuf2dict(snapshot.pose)


def verify_color_image(result, snapshot):
    # TODO: read image from file and compare
    assert result['width'] == snapshot.color_image.width
    assert result['height'] == snapshot.color_image.height
    assert os.path.isfile(result['path'])


def verify_depth_image(result, snapshot):
    # TODO: read image from file and compare
    assert os.path.isfile(result['path'])


def verify_feelings(result, snapshot):
    assert result == protobuf2dict(snapshot.feelings)


def test_pose(random_snapshot):
    snapshot, data, _ = random_snapshot
    result = run_parser('pose', data)
    verify_result_header(result, snapshot)
    verify_pose(result['result'], snapshot)


def test_color_image(random_snapshot):
    # TODO: read image from file and compare
    snapshot, data, _ = random_snapshot
    result = run_parser('color_image', data)
    verify_result_header(result, snapshot)
    verify_color_image(result['result'], snapshot)


def test_depth_image(random_snapshot):
    # TODO: read image from file and compare
    snapshot, data, _ = random_snapshot
    result = run_parser('depth_image', data)
    verify_result_header(result, snapshot)
    verify_depth_image(result['result'], snapshot)


def test_feelings(random_snapshot):
    snapshot, data, _ = random_snapshot
    result = run_parser('feelings', data)
    verify_result_header(result, snapshot)
    verify_feelings(result['result'], snapshot)


class MockMQAgent:
    snapshot = None
    result = None

    def __init__(self, url):
        pass

    def consume_snapshots(self, callback, topic):
        callback(self.__class__.snapshot)

    def publish_result(self, result, topic):
        self.__class__.result = result

    @classmethod
    def clear(cls):
        cls.snapshot = cls.result = None


@pytest.fixture
def mock_mq_agent(monkeypatch):
    yield monkeypatch.setattr(brain.parsers.parsers, 'MQAgent', MockMQAgent)
    MockMQAgent.clear()


@pytest.mark.parametrize('parser', ['pose', 'color_image', 'depth_image', 'feelings'])
def test_invoke_parser(parser, mock_mq_agent, random_snapshot):
    snapshot, data, _ = random_snapshot
    MockMQAgent.snapshot = data
    invoke_parser(parser, MQ_URL)
    result = MockMQAgent.result
    result = json.loads(result)
    verify_result_header(result, snapshot)
    result = result['result']
    if parser == 'pose':
        verify_pose(result, snapshot)
    elif parser == 'color_image':
        verify_color_image(result, snapshot)
    elif parser == 'depth_image':
        verify_depth_image(result, snapshot)
    elif parser == 'feelings':
        verify_feelings(result, snapshot)


@pytest.fixture
def mock_rabbitmq(monkeypatch):
    def expected_callback(data):
        pass

    expected_data = 'Expected data'

    class MockRabbitMQ:
        def __init__(self, url):
            assert url == MQ_URL

        def consume(self, callback, exchange, queues, exchange_type='fanout'):
            assert callback == expected_callback
            assert exchange == 'snapshot'
            assert queues == ['pose']

        def publish(self, data, exchange='', queue=''):
            assert data == expected_data
            assert exchange == 'saver'
            assert queue == 'saver_pose'

    monkeypatch.setattr(brain.parsers.mq_agent, 'RabbitMQ', MockRabbitMQ)
    yield expected_callback, expected_data


def test_mq_agent(mock_rabbitmq):
    expected_callback, expected_data = mock_rabbitmq
    mq_agent = MQAgent(MQ_URL)
    mq_agent.consume_snapshots(expected_callback, 'pose')
    mq_agent.publish_result(expected_data, 'pose')


@pytest.fixture
def mock_invoke_parser(monkeypatch):
    def fake_invoke_parser(parser, mq_url):
        assert parser == 'pose'
        assert mq_url == MQ_URL

    monkeypatch.setattr(brain.parsers.__main__, 'invoke_parser', fake_invoke_parser)


def test_cli(random_snapshot, mock_invoke_parser):
    snapshot, data, file_path = random_snapshot
    runner = CliRunner()
    for parser in PARSERS:
        result = runner.invoke(cli, ['parse', parser, file_path])
        assert result.exit_code == 0, result.exception
        parsed = json.loads(result.stdout)
        result_dict = parsed['result']
        if parser == 'pose':
            verify_pose(result_dict, snapshot)
        elif parser == 'color_image':
            verify_color_image(result_dict, snapshot)
        elif parser == 'depth_image':
            verify_depth_image(result_dict, snapshot)
        elif parser == 'feelings':
            verify_feelings(result_dict, snapshot)

    res = runner.invoke(cli, ['run-parser', 'pose', MQ_URL])
    assert res.exit_code == 0, res.exception
