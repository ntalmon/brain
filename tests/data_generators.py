import os
import pathlib
import random

import numpy as np

from brain.autogen import sample_pb2

first_names = ('John', 'Andy', 'Joe')
last_names = ('Johnson', 'Smith', 'Williams')

user_id_count = 0


def gen_user(user):
    global user_id_count
    user_id_count += 1
    user.user_id = user_id_count
    user.username = f'{random.choice(first_names)} {random.choice(last_names)}'
    user.birthday = random.getrandbits(32)
    user.gender = random.choice(sample_pb2.User.Gender.values())
    return user


def gen_pose(pose):
    pose.translation.x = random.uniform(-100, 100)
    pose.translation.y = random.uniform(-100, 100)
    pose.translation.z = random.uniform(-100, 100)
    pose.rotation.x = random.uniform(-100, 100)
    pose.rotation.y = random.uniform(-100, 100)
    pose.rotation.z = random.uniform(-100, 100)
    pose.rotation.w = random.uniform(-100, 100)
    return pose


def gen_color_image(color_image, fmt, path=None):
    color_image.width = random.randint(5, 10)
    color_image.height = random.randint(5, 10)
    data = os.urandom(color_image.width * color_image.height * 3)
    if fmt in ['reader', 'protocol']:
        color_image.data = data
    else:
        file_name = 'color_image.raw'
        file_path = str(path / file_name)
        with open(file_path, 'wb') as file:
            file.write(data)
        color_image.file_name = file_name
    return color_image


def gen_depth_image(depth_image, fmt, path=None):
    depth_image.width = random.randint(5, 10)
    depth_image.height = random.randint(5, 10)
    data = [float(random.uniform(-100, 100)) for i in range(depth_image.width * depth_image.height)]
    if fmt in ['reader', 'protocol']:
        depth_image.data[:] = data
    else:
        array = np.array(data).astype(np.float)
        file_name = 'depth_image'
        np.save(str(path / file_name), array)
        file_name = 'depth_image.npy'
        depth_image.file_name = file_name
    return depth_image


def gen_feelings(feelings):
    feelings.hunger = random.uniform(-1, 1)
    feelings.thirst = random.uniform(-1, 1)
    feelings.exhaustion = random.uniform(-1, 1)
    feelings.happiness = random.uniform(-1, 1)
    return feelings


uuid_counter = 0


def gen_snapshot(snapshot, fmt, tmp_path=None, should_gen_user=False):
    if should_gen_user:
        gen_user(snapshot.user)
    if fmt not in ['reader', 'protocol']:
        global uuid_counter
        uuid_counter += 1
        snapshot.uuid = uuid_counter
    if fmt in ['parser']:
        user_dir = tmp_path / str(snapshot.user.user_id)
        if not user_dir.exists():
            user_dir.mkdir()
        snapshot_dir = user_dir / str(snapshot.uuid)
        if not snapshot_dir.exists():
            snapshot_dir.mkdir()
        snapshot.path = str(snapshot_dir)
    snapshot.datetime = random.getrandbits(64)
    if fmt in ['parser']:
        path = pathlib.Path(snapshot.path)
    else:
        path = tmp_path
    gen_pose(snapshot.pose)
    gen_color_image(snapshot.color_image, fmt, path=path)
    gen_depth_image(snapshot.depth_image, fmt, path=path)
    gen_feelings(snapshot.feelings)
    snapshot.ParseFromString(snapshot.SerializeToString())  # "align" to protobuf formats
    return snapshot
