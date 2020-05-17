import gzip
import os
import struct
import sys

import pytest

from brain import tests_path as _tests_path
from brain.autogen import reader_pb2
from .data_generators import gen_user, gen_snapshot

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_resources_path = _tests_path / 'resources'
_sample_path = _resources_path / 'tests_sample.mind.gz'


@pytest.fixture(scope='session')
def tests_path():
    return _tests_path


@pytest.fixture(scope='session')
def resources_path():
    return _resources_path


@pytest.fixture(scope='session')
def sample_path():
    return _sample_path


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
