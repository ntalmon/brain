import pytest
from click.testing import CliRunner

import brain.server.__main__
import brain.server.mq_agent
import brain.server.server
from brain.server.__main__ import cli
from brain.autogen import protocol_pb2
from brain.server.client_agent import app
from brain.server.server import init_publish, construct_publish
from tests.data_generators import gen_snapshot

HOST = '127.0.0.1'
PORT = 8000
MQ_URL = 'rabbitmq://127.0.0.1:5672'


@pytest.fixture
def client_message():
    snapshot = gen_snapshot(protocol_pb2.Snapshot(), 'protocol', should_gen_user=True)
    return snapshot, snapshot.SerializeToString()


class MockRabbitMQ:
    publish_params = None

    def __init__(self, mq_url):
        pass

    def publish(self, data, exchange='', queue=''):
        MockRabbitMQ.publish_params = data, exchange, queue


@pytest.fixture
def mock_rabbitmq(monkeypatch):
    monkeypatch.setattr(brain.server.mq_agent, 'RabbitMQ', MockRabbitMQ)


def test_server(client_message, mock_rabbitmq):
    snapshot, msg = client_message
    publish = construct_publish(MQ_URL)
    init_publish(publish)

    with app.test_client() as client:
        res = client.post('/snapshot', data=msg)
        assert res.status_code == 200

    data, exchange, queue = MockRabbitMQ.publish_params
    assert exchange == 'snapshot'
    assert queue == ''
    # TODO: add data validation


class MockMQAgent:
    last_received_data = ''

    def __init__(self, mq_url):
        pass

    def publish_snapshot(self, data):
        self.__class__.last_received_data = data


def fake_run_server(host, port, publish):
    assert host == HOST
    assert port == PORT
    publish('Message to verify')


@pytest.fixture
def mock_run_server(monkeypatch):
    monkeypatch.setattr(brain.server.server, 'MQAgent', MockMQAgent)
    monkeypatch.setattr(brain.server.__main__, 'run_server', fake_run_server)


def test_cli(mock_run_server):
    runner = CliRunner()
    res = runner.invoke(cli, ['run-server', MQ_URL])
    assert res.exit_code == 0
    assert MockMQAgent.last_received_data == 'Message to verify'
