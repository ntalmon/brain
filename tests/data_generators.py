import os
import random
import threading

import numpy as np

from brain.autogen import reader_pb2

first_names = ('John', 'Andy', 'Joe')
last_names = ('Johnson', 'Smith', 'Williams')

user_id_count = 0


def gen_user(user):
    global user_id_count
    user_id_count += 1
    user.user_id = user_id_count
    user.username = f'{random.choice(first_names)} {random.choice(last_names)}'
    user.birthday = random.getrandbits(32)
    user.gender = random.choice(reader_pb2.User.Gender.values())
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


def gen_color_image(color_image, fmt, tmp_path=None):
    color_image.width = random.randint(5, 10)
    color_image.height = random.randint(5, 10)
    data = os.urandom(color_image.width * color_image.height * 3)
    if fmt in ['reader', 'protocol']:
        color_image.data = data
    else:
        file_path = str(tmp_path / 'color_image.raw')
        with open(file_path, 'wb') as file:
            file.write(data)
        color_image.path = file_path
    return color_image


def gen_depth_image(depth_image, fmt, tmp_path=None):
    depth_image.width = random.randint(5, 10)
    depth_image.height = random.randint(5, 10)
    data = [float(random.uniform(-100, 100)) for i in range(depth_image.width * depth_image.height)]
    if fmt in ['reader', 'protocol']:
        depth_image.data[:] = data
    else:
        array = np.array(data).astype(np.float)
        np.save(str(tmp_path / 'depth_image'), array)
        depth_image.path = str(tmp_path / 'depth_image.npy')
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
    snapshot.datetime = random.getrandbits(64)
    gen_pose(snapshot.pose)
    gen_color_image(snapshot.color_image, fmt, tmp_path=tmp_path)
    gen_depth_image(snapshot.depth_image, fmt, tmp_path=tmp_path)
    gen_feelings(snapshot.feelings)
    snapshot.ParseFromString(snapshot.SerializeToString())  # "align" to protobuf formats
    return snapshot
