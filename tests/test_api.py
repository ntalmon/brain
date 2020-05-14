import random

import pymongo
import pytest

from brain.api.api import app, init_db_agent
from brain.autogen import parsers_pb2
from tests.data_generators import gen_snapshot, gen_user
from tests.utils import protobuf2dict

DB_HOST = '127.0.0.1'
DB_PORT = 27017
DB_URL = f'mongodb://{DB_HOST}:{DB_PORT}'


@pytest.fixture
def populated_db(tmp_path):
    conn = pymongo.MongoClient(host=DB_HOST, port=DB_PORT)
    db = conn['brain']
    db.drop_collection('users')
    users = db['users']
    db_data = []
    for _ in range(5):
        user = gen_user(parsers_pb2.User())
        entry = protobuf2dict(user)
        entry['_id'] = entry['user_id']
        entry['snapshots'] = []
        for _ in range(5):
            snapshot = gen_snapshot(parsers_pb2.Snapshot(), 'parser', tmp_path=tmp_path)
            s_entry = protobuf2dict(snapshot)
            s_entry['_id'] = s_entry['uuid']
            s_entry['results'] = {}
            for result in ['pose', 'color_image', 'depth_image', 'feelings']:
                if result in s_entry:
                    s_entry['results'][result] = s_entry.pop(result)
            entry['snapshots'].append(s_entry)
        db_data.append(entry)
    users.insert_many(db_data)
    return db_data, users


def test_run_server():
    assert False


def api_get_and_compare(url, expected_json):
    with app.test_client() as client:
        res = client.get(url)
        assert res.status_code == 200
        assert res.json == expected_json


def test_get_users(populated_db):
    db_data, users = populated_db
    init_db_agent(DB_URL)
    expected = [{'user_id': entry['user_id'], 'username': entry['username']} for entry in db_data]
    api_get_and_compare('/users', expected)


def test_get_user(populated_db):
    db_data, users = populated_db
    init_db_agent(DB_URL)
    entry = random.choice(db_data)
    user_id = entry['user_id']
    expected = {'user_id': user_id, 'username': entry['username'], 'birthday': entry['birthday'],
                'gender': entry['gender']}
    api_get_and_compare(f'/users/{user_id}', expected)


def test_get_snapshots(populated_db):
    db_data, users = populated_db
    init_db_agent(DB_URL)
    entry = random.choice(db_data)
    user_id = entry['user_id']
    expected = [{'uuid': snapshot['uuid'], 'datetime': snapshot['datetime']} for snapshot in entry['snapshots']]
    api_get_and_compare(f'/users/{user_id}/snapshots', expected)


def test_get_snapshot(populated_db):
    db_data, users = populated_db
    init_db_agent(DB_URL)
    entry = random.choice(db_data)
    user_id = entry['user_id']
    snapshot = random.choice(entry['snapshots'])
    uuid = snapshot['uuid']
    expected = {'uuid': uuid, 'datetime': snapshot['datetime'], 'results': list(snapshot['results'].keys())}
    api_get_and_compare(f'/users/{user_id}/snapshots/{uuid}', expected)


def test_get_result(populated_db):
    db_data, users = populated_db
    init_db_agent(DB_URL)
    entry = random.choice(db_data)
    user_id = entry['user_id']
    snapshot = random.choice(entry['snapshots'])
    uuid = snapshot['uuid']
    for topic, result in snapshot['results'].items():
        api_get_and_compare(f'/users/{user_id}/snapshots/{uuid}/{topic}', result)


def test_get_result_data(populated_db):
    db_data, users = populated_db
    init_db_agent(DB_URL)
    entry = random.choice(db_data)
    user_id = entry['user_id']
    snapshot = random.choice(entry['snapshots'])
    uuid = snapshot['uuid']
    for topic in ['color_image', 'depth_image']:
        with app.test_client() as client:
            res = client.get(f'/users/{user_id}/snapshots/{uuid}/{topic}/data')
            assert res.status_code == 200
            assert res.mimetype == 'image/jpeg'
            result = snapshot['results'][topic]
            with open(result['path'], 'rb') as file:
                file_data = file.read()
            assert res.data == file_data


def test_cli():
    assert False
