import gzip
import random
import struct

import pytest

from brain.autogen import reader_pb2


def _write_message(writer, message):
    size = len(message)
    data = struct.pack('I', size) + message
    return writer.write(data)  # TODO: handle possible exceptions


@pytest.fixture
def mind_file(tmp_path, random_user, snapshot_generator):
    path = tmp_path / 'sample.mind.gz'
    with gzip.open(str(path), 'w') as file:
        msg = random_user.SerializeToString()
        _write_message(file, msg)
        for snapshot in snapshot_generator(5):
            msg = snapshot.SerializeToString()
            _write_message(file, msg)
    return tmp_path


def _gen_random_pose():
    pose = reader_pb2.Pose()
    pose.translation.x = random.uniform(-100, 100)
    pose.translation.y = random.uniform(-100, 100)
    pose.translation.z = random.uniform(-100, 100)
    pose.rotation.x = random.uniform(-100, 100)
    pose.rotation.y = random.uniform(-100, 100)
    pose.rotation.z = random.uniform(-100, 100)
    pose.rotation.w = random.uniform(-100, 100)
    return pose


def _gen_random_bytes(num_bytes):
    with open('/dev/urandom', 'rb') as file:
        data = file.read(num_bytes)
    return data


def _gen_random_color_image():
    color_image = reader_pb2.ColorImage()
    color_image.width = random.randint(1, 100)
    color_image.height = random.randint(1, 100)
    color_image.data = _gen_random_bytes(color_image.width * color_image.height * 3)
    return color_image


def _gen_random_depth_image():
    depth_image = reader_pb2.DepthImage()
    depth_image.width = random.randint(1, 100)
    depth_image.height = random.randint(1, 100)
    depth_image.data = [random.uniform(-100, 100) for i in range(depth_image.width * depth_image.height)]
    return depth_image


def _gen_random_feelings():
    feelings = reader_pb2.Feelings()
    feelings.hunger = random.uniform(-1, 1)
    feelings.thirst = random.uniform(-1, 1)
    feelings.exhaustion = random.uniform(-1, 1)
    feelings.happiness = random.uniform(-1, 1)
    return feelings


def _gen_random_snapshot():
    snapshot = reader_pb2.Snapshot()
    snapshot.datetime = random.getrandbits(64)
    snapshot.pose = _gen_random_pose()
    snapshot.color_image = _gen_random_color_image()
    snapshot.depth_image = _gen_random_depth_image()
    snapshot.feelings = _gen_random_feelings()
    return snapshot
