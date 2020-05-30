import pytest
from click.testing import CliRunner

import brain.server.__main__
import brain.server.mq_agent.rabbitmq_agent
import brain.server.parsers_agent
import brain.server.server
from brain.server.__main__ import cli
from brain.server.client_agent import load_client_agent
from brain.server.server import construct_publish, handle_snapshot
from brain.utils.consts import *
from .data_generators import gen_snapshot_for_server


@pytest.fixture
def client_message():
    snapshot = gen_snapshot_for_server(should_gen_user=True)
    return snapshot, snapshot.SerializeToString()


class MockRabbitMQ:
    publish_params = None

    def __init__(self, mq_url):
        pass

    def publish(self, data, exchange='', queue=''):
        MockRabbitMQ.publish_params = data, exchange, queue


@pytest.fixture
def mock_rabbitmq(monkeypatch):
    monkeypatch.setattr(brain.server.mq_agent.rabbitmq_agent, 'RabbitMQ', MockRabbitMQ)


@pytest.fixture
def mock_path(monkeypatch, tmp_path):
    monkeypatch.setattr(brain.server.parsers_agent, 'data_path', tmp_path)


def test_server(client_message, mock_rabbitmq, mock_path):
    snapshot, msg = client_message
    publish = construct_publish(MQ_URL)
    client_agent_module = load_client_agent('http')
    client_agent = client_agent_module.ClientAgent(publish)
    client_agent.register_snapshot_handler(handle_snapshot)

    with client_agent.app.test_client() as client:
        res = client.post('/snapshot', data=msg)
        assert res.status_code == 200

    data, exchange, queue = MockRabbitMQ.publish_params
    assert exchange == 'snapshot'
    assert queue == ''


class MockMQAgent:
    last_received_data = ''

    def __init__(self, mq_url):
        pass

    def publish_snapshot(self, data):
        self.__class__.last_received_data = data


def fake_run_server(host, port, publish):
    assert host == SERVER_HOST
    assert port == SERVER_PORT
    publish('Message to verify')


@pytest.fixture
def mock_run_server(monkeypatch):
    monkeypatch.setattr(brain.server.mq_agent.rabbitmq_agent, 'MQAgent', MockMQAgent)
    monkeypatch.setattr(brain.server.__main__, 'run_server', fake_run_server)


def test_cli(mock_run_server):
    runner = CliRunner()
    res = runner.invoke(cli, ['run-server', MQ_URL])
    assert res.exit_code == 0
    assert MockMQAgent.last_received_data == 'Message to verify'
