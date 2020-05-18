import time

import pytest

from brain.utils.mq.rabbitmq import RabbitMQ
from tests.utils import run_in_background

MQ_URL = 'rabbitmq://127.0.0.1:5672'


@pytest.fixture
def rabbit():
    return RabbitMQ(MQ_URL)


class TestRabbitMQ:
    rabbit = None  # type: RabbitMQ

    @classmethod
    def setup_class(cls):
        cls.rabbit = RabbitMQ(MQ_URL)

    @classmethod
    def teardown_class(cls):
        cls.rabbit.close()

    @pytest.fixture
    def simple_consume(self):
        def wrapper(pipe):
            pipe.send('ready')

            def callback(data):
                pipe.send(data)

            self.rabbit.consume(callback, '', ['q1'])

        yield from run_in_background(wrapper, poll=2)

    def test_consume(self, simple_consume):
        msg = b'Message from publisher!'
        time.sleep(1)
        self.rabbit.publish(msg, queue='q1')
        data = simple_consume()
        assert data == msg

    @pytest.fixture
    def simple_fanout(self):
        def wrapper(pipe):
            pipe.send('ready')

            def callback(data):
                pipe.send(data)

            self.rabbit.consume(callback, 'e1', ['q2', 'q3'])

        yield from run_in_background(wrapper, poll=2)

    def test_fanout(self, simple_fanout):
        msg = b'Message from publisher!'
        time.sleep(1)
        self.rabbit.publish(msg, exchange='e1')
        assert simple_fanout() == msg
        assert simple_fanout() == msg
