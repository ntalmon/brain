import gzip
import struct

import pytest

import brain.client.client
from brain.autogen import protocol_pb2
from brain.client import upload_sample
from brain.client.reader import Reader
from brain.client.server_agent import ServerAgent
from tests.data_generators import gen_client_user, gen_client_snapshot
from tests.utils import cmp_protobuf

HOST = '127.0.0.1'
PORT = 8000


class MockReader:
    _user = None
    _snapshots = []

    def __init__(self, path):
        self.path = path
        self._count = 0

    def load(self):
        user = gen_client_user()
        self.__class__._user = user
        return user

    def __iter__(self):
        return self

    def __next__(self):
        self._count += 1
        if self._count > 5:
            raise StopIteration()
        snapshot = gen_client_snapshot()
        self.__class__._snapshots.append(snapshot)
        return snapshot

    @classmethod
    def clear(cls):
        cls._user = None
        cls._snapshots = []


@pytest.fixture
def mock_reader(monkeypatch):
    yield monkeypatch.setattr(brain.client.client, 'Reader', MockReader)
    MockReader.clear()


class MockServerAgent:
    _users = []
    _snapshots = []

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_snapshot(self, user, snapshot):
        if user not in self.__class__._users:
            self.__class__._users.append(user)
        self.__class__._snapshots.append(snapshot)

    @classmethod
    def clear(cls):
        cls._users = []
        cls._snapshots = []


@pytest.fixture
def mock_server_agent(monkeypatch):
    yield monkeypatch.setattr(brain.client.client, 'ServerAgent', MockServerAgent)
    MockServerAgent.clear()


def test_upload_sample(mock_reader, mock_server_agent, tmp_path):
    upload_sample(HOST, PORT, str(tmp_path))
    assert len(MockServerAgent._users) == 1
    assert cmp_protobuf(MockServerAgent._users[0], MockReader._user)
    agent_snapshots = MockServerAgent._snapshots
    reader_snapshots = MockReader._snapshots
    assert len(agent_snapshots) == len(reader_snapshots)
    for agent_snapshot, reader_snapshot in zip(agent_snapshots, reader_snapshots):
        assert cmp_protobuf(agent_snapshot, reader_snapshot)


@pytest.fixture
def reader_sample(tmp_path):
    user = gen_client_user()
    snapshots = [gen_client_snapshot() for _ in range(5)]
    file_path = tmp_path / 'sample.mind.gz'
    with gzip.open(str(file_path), 'wb') as writer:
        user_msg = user.SerializeToString()
        user_msg = struct.pack('I', len(user_msg)) + user_msg
        writer.write(user_msg)
        for snapshot in snapshots:
            snapshot_msg = snapshot.SerializeToString()
            snapshot_msg = struct.pack('I', len(snapshot_msg)) + snapshot_msg
            writer.write(snapshot_msg)
    return str(file_path), user, snapshots


def test_reader(reader_sample):
    file_path, expected_user, expected_snapshots = reader_sample
    reader = Reader(file_path)
    user = reader.load()
    assert cmp_protobuf(user, expected_user)
    count = 0

    for snapshot, expected_snapshot in zip(reader, expected_snapshots):
        count += 1
        assert cmp_protobuf(snapshot, expected_snapshot)

    assert count == len(expected_snapshots)


def fake_post(url, data):
    fake_post.url = url
    fake_post.data = data
    return 200


@pytest.fixture
def mock_post(monkeypatch):
    yield monkeypatch.setattr(brain.client.server_agent, 'post', fake_post)
    del fake_post.url
    del fake_post.data


@pytest.fixture
def server_agent_sample():
    user = gen_client_user()
    snapshot = gen_client_snapshot()
    return user, snapshot


def test_server_agent(mock_post, server_agent_sample):
    user, snapshot = server_agent_sample
    agent = ServerAgent(HOST, PORT)
    agent.send_snapshot(user, snapshot)

    assert hasattr(fake_post, 'url') and hasattr(fake_post, 'data'), 'fake_post has never been called'
    assert fake_post.url.host == HOST
    assert fake_post.url.port == PORT
    data = fake_post.data
    new_snapshot = protocol_pb2.Snapshot()
    new_snapshot.ParseFromString(data)

    assert new_snapshot.datetime == snapshot.datetime
    assert cmp_protobuf(new_snapshot.user, user)
    assert cmp_protobuf(new_snapshot.pose, snapshot.pose)
    assert cmp_protobuf(new_snapshot.color_image, snapshot.color_image)
    assert cmp_protobuf(new_snapshot.depth_image, snapshot.depth_image)
    assert cmp_protobuf(new_snapshot.feelings, snapshot.feelings)


def test_cli():
    assert False
