import json

import pytest
import brain.saver.saver
from brain.autogen import parsers_pb2
from brain.saver import Saver
from tests.data_generators import gen_user, gen_snapshot
from tests.utils import protobuf2dict, dict_projection

DB_URL = 'mongodb://127.0.0.1:27017'
MQ_URL = 'rabbitmq://127.0.0.1:5672'
PARSERS = ['pose', 'color_image', 'depth_image', 'feelings']


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


@pytest.fixture
def random_results(tmp_path):
    users_snapshots = {}
    all_results = []
    for i in range(5):
        user = gen_user(parsers_pb2.User())
        user = protobuf2dict(user)
        users_snapshots[user['user_id']] = {'user': user, 'snapshots': []}
        for j in range(5):
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


def compare_db(database, users_snapshots):
    users = database['users']
    collection = users.find({})
    collection = list(collection)
    for user_id, items in users_snapshots.items():
        for user_entry in collection:
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
    yield monkeypatch.setattr(brain.saver.saver, 'MQAgent', MockMQAgent)
    MockMQAgent.clear()


# def test_run_saver(parser, mock_mq_agent, random_snapshot):
#     snapshot, data = random_snapshot
#     MockMQAgent.snapshot = data
#     run_saver(DB_URL, MQ_URL)
#     result = MockMQAgent.result
#     result = json.loads(result)
#     verify_result_header(result, snapshot)
#     result = result['result']
#     if parser == 'pose':
#         verify_pose(result, snapshot)
#     elif parser == 'color_image':
#         verify_color_image(result, snapshot)
#     elif parser == 'depth_image':
#         verify_depth_image(result, snapshot)
#     else:
#         verify_feelings(result, snapshot)


def test_run_saver():
    assert False


def test_cli():
    assert False
