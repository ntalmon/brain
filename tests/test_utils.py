import threading
import time

import flask
import pika
import pytest

from brain.utils.consts import *
from brain.utils.http import get, post
from brain.utils.rabbitmq import RabbitMQ
from .utils import run_in_background, add_shutdown_to_app, shutdown_server, wait_for_address


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

    def test_exceptions(self):
        with pytest.raises(pika.connection.exceptions.AMQPError):
            RabbitMQ.connect(MQ_HOST, 1234, max_retries=3)


@pytest.fixture
def simple_app():
    app = flask.Flask(__name__)
    add_shutdown_to_app(app)

    @app.route('/', methods=['GET', 'POST'])
    def default():
        return 'xyz'

    thr = threading.Thread(target=lambda: app.run(host='127.0.0.1', port=8003))
    thr.start()
    wait_for_address('127.0.0.1', 8003)
    url = 'http://127.0.0.1:8003'
    yield url
    shutdown_server(url)
    thr.join(timeout=30)


def test_get(simple_app):
    res = get(f'{simple_app}/')
    assert res == 'xyz'
    with pytest.raises(Exception) as error:
        get(f'{simple_app}/bad_path')
    assert 'failed with exit-code' in str(error.value)


def test_post(simple_app):
    res = post(f'{simple_app}/', 'abc')
    assert res == 'xyz'
    with pytest.raises(Exception) as error:
        post(f'{simple_app}/bad_path', 'abc')
    assert 'failed with exit-code' in str(error.value)
