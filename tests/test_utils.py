import threading
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

            self.rabbit.consume(callback, queue='q1')

        yield from run_in_background(wrapper, poll=2)

    def test_consume(self, simple_consume):
        msg = b'Message from publisher!'
        self.rabbit.publish(msg, queue='q1')
        data = simple_consume()
        assert data == msg

    @pytest.fixture
    def simple_multi_consume(self):
        def wrapper(pipe):
            pipe.send('ready')

            pipe_lock = threading.Lock()

            def callback(queue, data):
                with pipe_lock:
                    pipe.send((queue, data))

            self.rabbit.multi_consume(callback, queues=['q3', 'q4'])

        yield from run_in_background(wrapper, poll=2)

    def test_multi_consume(self, simple_multi_consume):
        msg = b'Message from publisher!'
        self.rabbit.publish(msg, queue='q3')
        self.rabbit.publish(msg, queue='q4')
        collected = set()
        collected.add(simple_multi_consume())
        collected.add(simple_multi_consume())
        expected = {('q3', msg), ('q4', msg)}
        assert collected == expected
