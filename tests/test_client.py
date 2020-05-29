import gzip
import pathlib
import struct

import pytest
from click.testing import CliRunner

import brain.client.server_agent
from brain.autogen import client_server_pb2
from brain.client import upload_sample
from brain.client.__main__ import cli
from brain.client.reader import Reader
from brain.utils.consts import *


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
    upload_sample(SERVER_HOST, SERVER_PORT, file_path)
    calls = mock_server
    assert len(calls) == len(snapshots)
    for call, snapshot in zip(calls, snapshots):
        url, data = call
        result = client_server_pb2.Snapshot()
        result.ParseFromString(data)
        assert result.datetime == snapshot.datetime
        assert str(result.user) == str(user)
        assert str(result.pose) == str(snapshot.pose)
        assert str(result.color_image) == str(snapshot.color_image)
        assert str(result.depth_image) == str(snapshot.depth_image)
        assert str(result.feelings) == str(snapshot.feelings)


def test_reader(random_sample, tmp_path):
    user, snapshots, file_path = random_sample
    reader1 = Reader(file_path)
    with pytest.raises(Exception) as error:
        for _ in reader1:
            pass
    assert f'Reader is unloaded' in str(error.value)
    user1 = reader1.load()
    assert reader1.load() == user1

    reader2 = Reader(str(tmp_path / 'file_not_exist.mind.gz'))
    with pytest.raises(OSError):
        reader2.load()

    empty_file = tmp_path / 'empty_file.mind.gz'
    with gzip.open(str(empty_file), 'wb'):
        pass
    reader3 = Reader(str(empty_file))
    with pytest.raises(Exception) as error:
        reader3.load()
    assert f'missing header' in str(error.value).lower()

    bad_msg_file = tmp_path / 'bad_msg.mind.gz'
    with gzip.open(str(bad_msg_file), 'wb') as file:
        file.write(struct.pack('I', 4) + b'xyz')
    reader4 = Reader(str(bad_msg_file))
    with pytest.raises(Exception) as error:
        reader4.load()
    assert 'expected to read' in str(error.value).lower()

    bad_size_file = tmp_path / 'bad_msg.mind.gz'
    with gzip.open(str(bad_msg_file), 'wb') as file:
        file.write(struct.pack('I', 1)[:3])
    reader5 = Reader(str(bad_size_file))
    with pytest.raises(Exception) as error:
        reader5.load()
    assert f'failed to read message size' in str(error.value).lower()

    bad_format_file = tmp_path / 'bad_format_file.mind.gz'
    with gzip.open(str(bad_format_file), 'wb') as file:
        file.write(struct.pack('I', 4) + b'abcd')
    reader6 = Reader(str(bad_format_file))
    with pytest.raises(Exception) as error:
        reader6.load()
    assert f'failed to parse protobuf' in str(error.value).lower()


def test_cli(resources_path, mock_server):
    sample_path = resources_path / 'tests_sample.mind.gz'
    runner = CliRunner()
    result = runner.invoke(cli, ['upload-sample', str(sample_path)])
    assert result.exit_code == 0
    assert f'snapshots successfully uploaded' in result.output
