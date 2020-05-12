import gzip
import multiprocessing
import struct
import subprocess

import flask
import pytest
import brain.client.server_agent

from brain.autogen import reader_pb2, protocol_pb2
from brain.client import upload_sample
from tests.data_generators import gen_user, gen_snapshot

HOST = '127.0.0.1'
PORT = 8000


@pytest.fixture
def mock_server(monkeypatch):
    calls = []

    def mock_post(url, data):
        calls.append((url, data))
        return 200

    monkeypatch.setattr(brain.client.server_agent, 'post', mock_post)
    return calls


def write_sample(user, snapshots, path):
    file_path = str(path / 'sample.mind.gz')
    user_raw = user.SerializeToString()
    snapshots_raw = [snapshot.SerializeToString() for snapshot in snapshots]
    with gzip.open(file_path, 'wb') as file:
        file.write(struct.pack('I', len(user_raw)) + user_raw)
        for snapshot_raw in snapshots_raw:
            file.write(struct.pack('I', len(snapshot_raw)) + snapshot_raw)

    return file_path


@pytest.fixture
def random_sample(tmp_path):
    user = gen_user(reader_pb2.User())
    snapshots = [gen_snapshot(reader_pb2.Snapshot(), 'reader', tmp_path=tmp_path) for _ in range(5)]
    file_path = write_sample(user, snapshots, tmp_path)
    return user, snapshots, file_path


def test_client(random_sample, mock_server):
    user, snapshots, file_path = random_sample
    upload_sample(HOST, PORT, file_path)
    calls = mock_server
    assert len(calls) == len(snapshots)
    for call, snapshot in zip(calls, snapshots):
        url, data = call
        result = protocol_pb2.Snapshot()
        result.ParseFromString(data)
        assert result.datetime == snapshot.datetime
        assert str(result.user) == str(user)
        assert str(result.pose) == str(snapshot.pose)
        assert str(result.color_image) == str(snapshot.color_image)
        assert str(result.depth_image) == str(snapshot.depth_image)
        assert str(result.feelings) == str(snapshot.feelings)


def _run_server(pipe):
    app = flask.Flask(__name__)
    pipe.send('ready')

    @app.route('/snapshot', methods=['GET', 'POST'])
    def route_snapshot():
        data = flask.request.data
        pipe.send(data)
        return ''

    app.run(host=HOST, port=PORT)


@pytest.fixture
def get_message():
    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=_run_server, args=(child,))
    process.start()
    parent.recv()
    try:
        def get_message():
            if not parent.poll(1):
                raise TimeoutError()
            return parent.recv()

        yield get_message
    finally:
        process.terminate()
        process.join()


def test_cli(get_message, resources_path):
    sample_file = resources_path / 'tests_sample.mind.gz'
    cmd = ['python', '-m', 'brain.client', 'upload-sample', '-h', HOST, '-p', str(PORT), str(sample_file)]
    import time
    time.sleep(3)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)

    stdout, _ = process.communicate()
    assert b'all snapshots uploaded successfully' in stdout.lower()
    data = get_message()
