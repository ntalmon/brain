import random

import numpy as np

from brain.autogen import reader_pb2, parsers_pb2

first_names = ('John', 'Andy', 'Joe')
last_names = ('Johnson', 'Smith', 'Williams')


def _gen_user_name():
    return f'{random.choice(first_names)} {random.choice(last_names)}'


def gen_client_user():
    user = reader_pb2.User()
    user.user_id = random.randint(0, 100)
    user.username = _gen_user_name()
    user.birthday = random.getrandbits(32)
    user.gender = random.choice(reader_pb2.User.Gender.values())
    return user


def _gen_random_bytes(num_bytes):
    with open('/dev/urandom', 'rb') as file:
        data = file.read(num_bytes)
    return data


def gen_client_snapshot():
    snapshot = reader_pb2.Snapshot()
    snapshot.datetime = random.getrandbits(64)
    snapshot.pose.translation.x = random.uniform(-100, 100)
    snapshot.pose.translation.y = random.uniform(-100, 100)
    snapshot.pose.translation.z = random.uniform(-100, 100)
    snapshot.pose.rotation.x = random.uniform(-100, 100)
    snapshot.pose.rotation.y = random.uniform(-100, 100)
    snapshot.pose.rotation.z = random.uniform(-100, 100)
    snapshot.pose.rotation.w = random.uniform(-100, 100)
    snapshot.color_image.width = random.randint(1, 100)
    snapshot.color_image.height = random.randint(1, 100)
    snapshot.color_image.data = _gen_random_bytes(snapshot.color_image.width * snapshot.color_image.height * 3)
    snapshot.depth_image.width = random.randint(1, 100)
    snapshot.depth_image.height = random.randint(1, 100)
    snapshot.depth_image.data[:] = [float(random.uniform(-100, 100)) for i in
                                    range(snapshot.depth_image.width * snapshot.depth_image.height)]
    snapshot.feelings.hunger = random.uniform(-1, 1)
    snapshot.feelings.thirst = random.uniform(-1, 1)
    snapshot.feelings.exhaustion = random.uniform(-1, 1)
    snapshot.feelings.happiness = random.uniform(-1, 1)
    return snapshot


def gen_server_snapshot(tmp_path):
    snapshot = parsers_pb2.Snapshot()
    snapshot.uuid = random.randint(1, 100)
    snapshot.datetime = random.getrandbits(64)
    snapshot.user.user_id = random.randint(0, 100)
    snapshot.user.username = _gen_user_name()
    snapshot.user.birthday = random.getrandbits(32)
    snapshot.user.gender = random.choice(reader_pb2.User.Gender.values())
    snapshot.pose.translation.x = random.uniform(-100, 100)
    snapshot.pose.translation.y = random.uniform(-100, 100)
    snapshot.pose.translation.z = random.uniform(-100, 100)
    snapshot.pose.rotation.x = random.uniform(-100, 100)
    snapshot.pose.rotation.y = random.uniform(-100, 100)
    snapshot.pose.rotation.z = random.uniform(-100, 100)
    snapshot.pose.rotation.w = random.uniform(-100, 100)
    snapshot.color_image.width = random.randint(1, 100)
    snapshot.color_image.height = random.randint(1, 100)
    data = _gen_random_bytes(snapshot.color_image.width * snapshot.color_image.height * 3)
    snapshot.color_image.path = str(tmp_path / 'color_image.raw')
    with open(snapshot.color_image.path, 'wb') as writer:
        writer.write(data)
    snapshot.depth_image.width = random.randint(1, 100)
    snapshot.depth_image.height = random.randint(1, 100)
    data = [float(random.uniform(-100, 100)) for i in range(snapshot.depth_image.width * snapshot.depth_image.height)]
    array = np.array(data).astype(np.float)
    np.save(str(tmp_path / 'depth_image'), array)
    snapshot.depth_image.path = str(tmp_path / 'depth_image.npy')
    snapshot.feelings.hunger = random.uniform(-1, 1)
    snapshot.feelings.thirst = random.uniform(-1, 1)
    snapshot.feelings.exhaustion = random.uniform(-1, 1)
    snapshot.feelings.happiness = random.uniform(-1, 1)
    return snapshot
