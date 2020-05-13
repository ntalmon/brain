import pytest

import brain.server.mq_agent
from brain.autogen import protocol_pb2, parsers_pb2
from brain.server.client_agent import app
from brain.server.server import init_publish, construct_publish
from tests.data_generators import gen_snapshot

HOST = 'localhost'
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
