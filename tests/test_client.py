import gzip
import os
import random
import struct

import pytest
import brain.client.server_agent

from brain.autogen import reader_pb2, protocol_pb2
from brain.client import upload_sample

first_names = ('John', 'Andy', 'Joe')
last_names = ('Johnson', 'Smith', 'Williams')
HOST = '127.0.0.1'
PORT = 8000


def _gen_random_user():
    return {
        'user_id': random.randint(0, 100),
        'username': f'{random.choice(first_names)} {random.choice(last_names)}',
        'birthday': random.getrandbits(32),
        'gender': random.randint(0, 2)
    }


def _gen_pose():
    return {
        'translation': {
            'x': float(random.uniform(-100, 100)),
            'y': float(random.uniform(-100, 100)),
            'z': float(random.uniform(-100, 100))
        },
        'rotation': {
            'x': float(random.uniform(-100, 100)),
            'y': float(random.uniform(-100, 100)),
            'z': float(random.uniform(-100, 100)),
            'w': float(random.uniform(-100, 100))
        }
    }


def _gen_color_image():
    width = random.randint(5, 10)
    height = random.randint(5, 10)
    return {
        'width': width,
        'height': height,
        'data': os.urandom(width * height * 3)
    }


def _gen_depth_image():
    width = random.randint(5, 10)
    height = random.randint(5, 10)
    return {
        'width': width,
        'height': height,
        'data': [float(random.uniform(-100, 100)) for _ in range(width * height)]
    }


def _gen_feelings():
    return {
        'hunger': float(random.uniform(-1, 1)),
        'thirst': float(random.uniform(-1, 1)),
        'exhaustion': float(random.uniform(-1, 1)),
        'happiness': float(random.uniform(-1, 1))
    }


def _gen_random_snapshot():
    return {
        'pose': _gen_pose(),
        'color_image': _gen_color_image(),
        'depth_image': _gen_depth_image(),
        'feelings': _gen_feelings()
    }


def json2pb(js_dict, pb_obj, serialize=False):
    def recursion(_js_dict, _pb_obj):
        for key, value in _js_dict.items():
            if isinstance(value, dict):
                recursion(value, getattr(_pb_obj, key))
            elif isinstance(value, list):
                getattr(_pb_obj, key)[:] = value
            else:
                setattr(_pb_obj, key, value)

    recursion(js_dict, pb_obj)
    return pb_obj.SerializeToString() if serialize else pb_obj


def _write_sample(user, snapshots, path):
    file_path = str(path / 'sample.mind.gz')
    user_msg = json2pb(user, reader_pb2.User(), serialize=True)
    snapshots_msg = []
    for snapshot in snapshots:
        snapshot_msg = json2pb(snapshot, reader_pb2.Snapshot(), serialize=True)
        snapshots_msg.append(snapshot_msg)

    with gzip.open(file_path, 'wb') as writer:
        writer.write(struct.pack('I', len(user_msg)) + user_msg)
        for snapshot_msg in snapshots_msg:
            writer.write(struct.pack('I', len(snapshot_msg)) + snapshot_msg)

    return file_path


@pytest.fixture
def random_sample(tmp_path):
    user = _gen_random_user()
    snapshots = [_gen_random_snapshot() for _ in range(5)]
    file_path = _write_sample(user, snapshots, tmp_path)
    return user, snapshots, file_path


@pytest.fixture
def mock_server(monkeypatch):
    calls = []

    def mock_post(url, data):
        calls.append((url, data))
        return 200

    monkeypatch.setattr(brain.client.server_agent, 'post', mock_post)
    return calls


def test_client(random_sample, mock_server):
    user, snapshots, file_path = random_sample
    upload_sample(HOST, PORT, file_path)
    calls = mock_server
    assert len(calls) == len(snapshots)
    for call, snapshot in zip(calls, snapshots):
        url, data = call
        expected = protocol_pb2.Snapshot()
        json2pb(user, expected.user)
        json2pb(snapshot, expected)
        assert data == expected.SerializeToString()
