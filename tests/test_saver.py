import json

import pytest
from click.testing import CliRunner

import brain.saver.mq_agent
import brain.saver.saver
from brain.saver import Saver, run_saver
from brain.saver.__main__ import cli
from brain.utils.consts import *
from .data_generators import gen_data_for_saver


@pytest.fixture
def saver():
    return Saver(DB_URL)


@pytest.fixture(scope='module')
def random_results(tmp_path_factory):
    path = tmp_path_factory.mktemp('saver')
    return gen_data_for_saver(path, 5, 5)


def compare_db(database, users_snapshots):
    collection = database[COLLECTION_NAME]
    collection_data = collection.find({})
    collection_data = list(collection_data)
    for user_id, items in users_snapshots.items():
        for user_entry in collection_data:
            if user_entry['user_id'] == user_id:
                break
        else:
            assert False, f'Could not find user entry with user id {user_id}'
        expected_user = items['user']
        assert user_entry['username'] == expected_user['username']
        assert user_entry['birthday'] == expected_user['birthday']
        assert user_entry['gender'] == expected_user['gender']
        expected_snapshots = items['snapshots']
        for snapshot in expected_snapshots:
            uuid = snapshot['uuid']
            for snapshot_entry in user_entry['snapshots']:
                if snapshot_entry['uuid'] == uuid:
                    break
            else:
                assert False, f'Could not find snapshot entry with uuid {uuid}'
            assert snapshot_entry['datetime'] == snapshot['datetime']
            for parser in PARSERS:
                assert snapshot_entry['results'][parser] == snapshot[parser]


def test_save(saver, database, random_results):
    results, users_snapshots = random_results
    for result in results:
        key, value = result
        saver.save(key, json.dumps(value))

    compare_db(database, users_snapshots)


class MockRabbitMQ:
    results_to_send = []

    def __init__(self, url):
        pass

    def consume(self, callback, exchange, queues, exchange_type='fanout'):
        for result in self.__class__.results_to_send:
            queue, msg = result
            callback(queue, msg)

    @classmethod
    def clear(cls):
        cls.results_to_send = []


@pytest.fixture
def mock_rabbitmq(monkeypatch):
    yield monkeypatch.setattr(brain.saver.mq_agent, 'RabbitMQ', MockRabbitMQ)
    MockRabbitMQ.clear()


def test_run_saver(database, random_results, mock_rabbitmq):
    results, snapshots = random_results
    new_results = [(f'saver_{item[0]}', json.dumps(item[1])) for item in results]
    MockRabbitMQ.results_to_send = new_results
    run_saver(DB_URL, MQ_URL)
    compare_db(database, snapshots)


@pytest.fixture
def mock_run_saver(monkeypatch):
    def fake_run_saver(db, mq):
        assert db == DB_URL
        assert mq == MQ_URL

    monkeypatch.setattr(brain.saver.__main__, 'run_saver', fake_run_saver)


def test_cli(tmp_path, database, random_results, mock_run_saver):
    results, snapshots = random_results
    runner = CliRunner()
    for result in results:
        result_name, result_data = result
        file_path = str(tmp_path / f'{result_name}.raw')
        with open(file_path, 'w') as file:
            file.write(json.dumps(result_data))
        res = runner.invoke(cli, ['save', result_name, file_path])
        assert res.exit_code == 0
    compare_db(database, snapshots)
    res = runner.invoke(cli, ['run-saver', DB_URL, MQ_URL])
    assert res.exit_code == 0, res.exception
