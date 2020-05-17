import random
import threading
import time

import pymongo
import pytest
import requests
from click.testing import CliRunner

import brain.api.__main__

from brain.api.__main__ import cli
from brain.api.api import app, init_db_agent, run_api_server
from brain.autogen import parsers_pb2
from tests.data_generators import gen_snapshot, gen_user
from tests.utils import protobuf2dict, add_shutdown_to_app

API_HOST = '127.0.0.1'
API_PORT = 5000
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


@pytest.fixture
def api_server_in_thread():
    add_shutdown_to_app(app)
    exc = None  # type: Exception

    def wrapper():  # TODO: move this procedure to common utils?
        try:
            run_api_server(API_HOST, API_PORT, DB_URL)
        except Exception as error:
            nonlocal exc
            exc = error

    def poll_exc():
        if exc:
            raise exc

    thr = threading.Thread(target=wrapper)
    thr.start()
    # reasonable time to wait for flask app to start
    # TODO: is there a "correct" way to wait for the flask app?
    time.sleep(3)
    yield poll_exc
    res = requests.post(f'http://{API_HOST}:{API_PORT}/shutdown')
    poll_exc()
    thr.join(timeout=10)


def test_run_api_server(populated_db, api_server_in_thread):
    poll_exc = api_server_in_thread
    poll_exc()
    res = requests.get(f'http://{API_HOST}:{API_PORT}/users')
    poll_exc()
    assert res.status_code == 200
    res = res.json()
    assert len(res) == 5


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


@pytest.fixture
def mock_run_api_server(monkeypatch):
    def fake_run_api_server(host, port, database):
        fake_run_api_server.host = host
        fake_run_api_server.port = port
        fake_run_api_server.database = database

    monkeypatch.setattr(brain.api.__main__, 'run_api_server', fake_run_api_server)
    yield fake_run_api_server


def test_cli(mock_run_api_server):
    runner = CliRunner()
    result = runner.invoke(cli, ['run-server', '-h', API_HOST, '-p', API_PORT, '-d', DB_URL])
    assert result.exit_code == 0
    assert mock_run_api_server.host == API_HOST
    assert mock_run_api_server.port == API_PORT
    assert mock_run_api_server.database == DB_URL
