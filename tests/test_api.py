import random

import pytest
import requests
from click.testing import CliRunner

import brain.api.__main__
from brain.api.__main__ import cli
from brain.api.api import app, init_db_agent, run_api_server, common_api_wrapper
from brain.utils.consts import *
from .data_generators import gen_db_data
from .utils import run_flask_in_thread, normalize_path


@pytest.fixture(scope='module')
def populated_db(database, tmp_path_factory):
    path = tmp_path_factory.mktemp('api')
    return gen_db_data(path, 5, 5, database=database)


def api_get_and_compare(url, code=200):
    with app.test_client() as client:
        res = client.get(url)
        assert res.status_code == code
        return res


def test_get_users(populated_db):
    db_data, collection = populated_db
    init_db_agent(DB_URL)
    expected = [{'user_id': entry['user_id'], 'username': entry['username']} for entry in db_data]
    res = api_get_and_compare('/users')
    assert res.json == expected


def test_get_user(populated_db):
    db_data, collection = populated_db
    init_db_agent(DB_URL)
    entry = random.choice(db_data)
    user_id = entry['user_id']
    expected = {'user_id': user_id, 'username': entry['username'], 'birthday': entry['birthday'],
                'gender': entry['gender']}
    res = api_get_and_compare(f'/users/{user_id}')
    assert res.json == expected


def test_get_snapshots(populated_db):
    db_data, collection = populated_db
    init_db_agent(DB_URL)
    entry = random.choice(db_data)
    user_id = entry['user_id']
    expected = [{'uuid': snapshot['uuid'], 'datetime': snapshot['datetime']} for snapshot in entry['snapshots']]
    res = api_get_and_compare(f'/users/{user_id}/snapshots')
    assert res.json == expected


def test_get_snapshot(populated_db):
    db_data, collection = populated_db
    init_db_agent(DB_URL)
    entry = random.choice(db_data)
    user_id = entry['user_id']
    snapshot = random.choice(entry['snapshots'])
    uuid = snapshot['uuid']
    expected = {'uuid': uuid, 'datetime': snapshot['datetime'], 'results': list(snapshot['results'].keys())}
    res = api_get_and_compare(f'/users/{user_id}/snapshots/{uuid}')
    assert res.json == expected


def test_get_result(populated_db):
    db_data, collection = populated_db
    init_db_agent(DB_URL)
    entry = random.choice(db_data)
    user_id = entry['user_id']
    snapshot = random.choice(entry['snapshots'])
    uuid = snapshot['uuid']
    for topic, result in snapshot['results'].items():
        res = api_get_and_compare(f'/users/{user_id}/snapshots/{uuid}/{topic}')
        assert res.json == result


def test_get_result_data(populated_db):
    db_data, collection = populated_db
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
            file_path = result['path']
            with open(file_path, 'rb') as file:
                file_data = file.read()
            assert res.data == file_data


@pytest.fixture
def api_server_in_thread():
    yield from run_flask_in_thread(app, API_URL, lambda: run_api_server(API_HOST, API_PORT, DB_URL))


def test_run_api_server(populated_db, api_server_in_thread):
    poll_exc = api_server_in_thread
    poll_exc()
    res = requests.get(f'{API_URL}/users', verify=False, timeout=5)
    poll_exc()
    assert res.status_code == 200
    res = res.json()
    assert len(res) == 5


@pytest.fixture
def mock_run_api_server(monkeypatch):
    def fake_run_api_server(host, port, database):
        fake_run_api_server.host = host
        fake_run_api_server.port = port
        fake_run_api_server.database = database

    monkeypatch.setattr(brain.api.__main__, 'run_api_server', fake_run_api_server)
    yield fake_run_api_server


@pytest.fixture
def mock_flask_abort(monkeypatch):
    def mock_abort(code):
        mock_abort.code = code

    monkeypatch.setattr(brain.api.api.flask, 'abort', mock_abort)
    return mock_abort


def test_common_api_wrapper(mock_flask_abort):
    def none_callback():
        return None

    def exception_callback():
        raise Exception()

    common_api_wrapper(none_callback)
    assert hasattr(mock_flask_abort, 'code'), 'Abort was not called'
    assert mock_flask_abort.code == 404

    delattr(mock_flask_abort, 'code')

    common_api_wrapper(exception_callback)
    assert hasattr(mock_flask_abort, 'code'), 'Abort was not called'
    assert mock_flask_abort.code == 500


@pytest.fixture
def populated_db_no_save(tmp_path):
    return gen_db_data(tmp_path, 1, 1)


def test_get_snapshot_result_data_file_name(database, populated_db_no_save):
    db_data = populated_db_no_save
    collection = database[COLLECTION_NAME]
    u_entry = db_data[0]
    s_entry = u_entry['snapshots'][0]
    r_entry = s_entry['results']['color_image']
    r_entry.pop('path')
    collection.insert_many(db_data)
    user_id = u_entry['user_id']
    snapshot_id = s_entry['uuid']
    url = f'/users/{user_id}/snapshots/{snapshot_id}/color_image/data'
    api_get_and_compare(url, code=404)


def test_get_snapshot_result_data_file_path(populated_db):
    db_data, collection = populated_db
    u_entry = db_data[0]
    s_entry = u_entry['snapshots'][0]
    r_entry = s_entry['results']['color_image']
    file_path = normalize_path(r_entry['path'])
    file_path.unlink()
    user_id = u_entry['user_id']
    snapshot_id = s_entry['uuid']
    url = f'/users/{user_id}/snapshots/{snapshot_id}/color_image/data'
    api_get_and_compare(url, code=404)


@pytest.fixture
def partially_populated_db(database):
    db_data = [
        {'_id': '1', 'user_id': '1', 'username': 'abc', 'birthday': 123, 'gender': 'MALE', 'snapshots': []},
        {'_id': '2', 'user_id': '2', 'username': 'abc', 'birthday': 123, 'gender': 'MALE',
         'snapshots': [{'_id': '1', 'uuid': '1', 'datetime': 123, 'results': {'feelings': {}}}]}
    ]
    collection = database[COLLECTION_NAME]
    backup = list(collection.find({}))
    collection.drop()
    collection.insert_many(db_data)
    yield
    collection.drop()
    collection.insert_many(backup)


def test_user_not_exist(partially_populated_db):
    init_db_agent(DB_URL)
    api_get_and_compare('/users/3/snapshots', code=404)
    api_get_and_compare('/users/3/snapshots/1', code=404)
    api_get_and_compare('/users/3/snapshots/1/color_image', code=404)
    api_get_and_compare('/users/1/snapshots/1', code=404)
    api_get_and_compare('/users/2/snapshots/1/color_image', code=404)


def test_cli(mock_run_api_server):
    runner = CliRunner()
    result = runner.invoke(cli, ['run-server', '-h', API_HOST, '-p', API_PORT, '-d', DB_URL])
    assert result.exit_code == 0
    assert mock_run_api_server.host == API_HOST
    assert mock_run_api_server.port == API_PORT
    assert mock_run_api_server.database == DB_URL
