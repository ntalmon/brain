import json

import pytest
from click.testing import CliRunner

import brain.saver.saver
import brain.saver.mq_agent
from brain.saver.__main__ import cli
from brain.autogen import parsers_pb2
from brain.saver import Saver, run_saver
from .consts import *
from .data_generators import gen_user, gen_snapshot
from .utils import protobuf2dict, dict_projection


@pytest.fixture
def saver():
    return Saver(DB_URL)


@pytest.fixture
def database():
    import pymongo
    conn = pymongo.MongoClient(DB_URL)
    conn.drop_database('brain')
    db = conn.brain
    yield db
    conn.close()


def gen_random_result(tmp_path, num_users, num_snapshots):
    users_snapshots = {}
    all_results = []
    for i in range(num_users):
        user = gen_user(parsers_pb2.User())
        user = protobuf2dict(user)
        users_snapshots[user['user_id']] = {'user': user, 'snapshots': []}
        for j in range(num_snapshots):
            snapshot = gen_snapshot(parsers_pb2.Snapshot(), 'parser', tmp_path=tmp_path)
            snapshot_dict = protobuf2dict(snapshot)
            users_snapshots[user['user_id']]['snapshots'].append(snapshot_dict)
            results = dict_projection(snapshot_dict, PARSERS)
            for key, value in results.items():
                all_results.append((key, {
                    'uuid': snapshot_dict['uuid'],
                    'datetime': snapshot_dict['datetime'],
                    'user': user,
                    'result': value
                }))
    return all_results, users_snapshots


@pytest.fixture
def random_results(tmp_path):
    return gen_random_result(tmp_path, 5, 5)


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
def random_result(tmp_path):
    return gen_random_result(tmp_path, 1, 1)


def test_cli(tmp_path, database, random_results):
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
