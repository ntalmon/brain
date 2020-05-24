import os
import pathlib
import random

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

from brain.autogen import sample_pb2, client_server_pb2, server_parsers_pb2
from brain.utils.consts import *
from .utils import normalize_path, align_protobuf, dict_projection

first_names = ('John', 'Andy', 'Joe')
last_names = ('Johnson', 'Smith', 'Williams')

user_id_count = 0


def gen_user(user=None):
    global user_id_count
    user_id_count += 1
    user_id = user_id_count
    username = f'{random.choice(first_names)} {random.choice(last_names)}'
    birthday = random.getrandbits(32)
    gender = random.choice(sample_pb2.User.Gender.values())
    if user:
        user.user_id, user.username, user.birthday, user.gender = user_id, username, birthday, gender
        return user
    return {'user_id': user_id, 'username': username, 'birthday': birthday, 'gender': gender}


def gen_pose(pose=None):
    t_x, t_y, t_z = [random.uniform(-100, 100) for _ in range(3)]
    r_x, r_y, r_z, r_w = [random.uniform(-100, 100) for _ in range(4)]
    if pose:
        t, r = pose.translation, pose.rotation
        t.x, t.y, t.z = t_x, t_y, t_z
        r.x, r.y, r.z, r.w = r_x, r_y, r_z, r_w
        return pose
    return {'translation': {'x': t_x, 'y': t_y, 'z': t_z}, 'rotation': {'x': r_x, 'y': r_y, 'z': r_z, 'w': r_w}}


def gen_color_image_base():
    width = random.randint(5, 10)
    height = random.randint(5, 10)
    data = os.urandom(width * height * 3)
    return width, height, data


def gen_color_image_data(color_image=None):
    width, height, data = gen_color_image_base()
    if color_image:
        color_image.width, color_image.height, color_image.data = width, height, data
        return color_image
    return {'width': width, 'height': height, 'data': data}


def gen_color_image_raw(path, color_image=None):
    width, height, data = gen_color_image_base()
    path = normalize_path(path)
    file_name = 'color_image.raw'
    file_path = str(path / file_name)
    with open(file_path, 'wb') as file:
        file.write(data)
    if color_image:
        color_image.width, color_image.height, color_image.file_name = width, height, file_name
        return color_image
    return {'width': width, 'height': height, 'file_name': file_name}


def gen_color_image_parsed(path, color_image=None):
    width, height, data = gen_color_image_base()
    path = normalize_path(path)
    file_name = 'color_image.jpg'
    file_path = str(path / file_name)
    image = Image.frombytes('RGB', (width, height), data)
    image.save(file_path)
    if color_image:
        color_image.width, color_image.height, color_image.path = width, height, file_path
    return {'width': width, 'height': height, 'path': file_path}


def gen_depth_image_base():
    width = random.randint(5, 10)
    height = random.randint(5, 10)
    data = [float(random.uniform(-100, 100)) for i in range(width * height)]
    return width, height, data


def gen_depth_image_data(depth_image=None):
    width, height, data = gen_depth_image_base()
    if depth_image:
        depth_image.width, depth_image.height, depth_image.data = width, height, data
        return depth_image
    return {'width': width, 'height': height, 'data': data}


def gen_depth_image_raw(path, depth_image=None):
    width, height, data = gen_depth_image_base()
    path = normalize_path(path)
    array = np.array(data).astype(np.float)
    np.save(str(path / 'depth_image'), array)
    file_name = 'depth_image.npy'
    if depth_image:
        depth_image.width, depth_image.height, depth_image.file_name = width, height, file_name
        return depth_image
    return {'width': width, 'height': height, 'file_name': file_name}


def gen_depth_image_parsed(path, depth_image=None):
    width, height, data = gen_depth_image_base()
    path = normalize_path(path)
    array = np.array(data).reshape((height, width))
    plt.imshow(array)
    file_path = str(path / 'depth_image.jpg')
    plt.savefig(file_path)
    if depth_image:
        depth_image.width, depth_image.height, depth_image.path = width, height, file_path
        return depth_image
    return {'width': width, 'height': height, 'path': file_path}


def gen_feelings(feelings=None):
    hunger, thirst, exhaustion, happiness = [random.uniform(-1, 1) for _ in range(4)]
    if feelings:
        feelings.hunger, feelings.thirst, feelings.exhaustion, feelings.happiness = hunger, thirst, exhaustion, \
                                                                                    happiness
        return feelings
    return {'hunger': hunger, 'thirst': thirst, 'exhaustion': exhaustion, 'happiness': happiness}


def gen_datetime(snapshot=None):
    dt = random.getrandbits(64)
    if snapshot:
        snapshot.datetime = dt
        return snapshot
    return dt


uuid_counter = 0


def gen_snapshot_id(snapshot=None):
    global uuid_counter
    uuid_counter += 1
    if snapshot:
        snapshot.uuid = uuid_counter
        return snapshot
    return uuid_counter


def get_snapshot_path(snapshot, path, is_dict=False):
    path = normalize_path(path)
    user_id = snapshot['user']['user_id'] if is_dict else snapshot.user.user_id
    user_dir = path / str(user_id)
    if not user_dir.exists():
        user_dir.mkdir()
    snapshot_id = snapshot['uuid'] if is_dict else snapshot.uuid
    snapshot_dir = user_dir / str(snapshot_id)
    if not snapshot_dir.exists():
        snapshot_dir.mkdir()
    return snapshot_dir


def gen_snapshot_for_client(snapshot=None):
    snapshot = snapshot or sample_pb2.Snapshot()
    gen_datetime(snapshot)
    gen_pose(snapshot.pose)
    gen_color_image_data(snapshot.color_image)
    gen_depth_image_data(snapshot.depth_image)
    align_protobuf(snapshot)
    return snapshot


def gen_snapshot_for_server(snapshot=None, should_gen_user=False):
    snapshot = snapshot or client_server_pb2.Snapshot()
    gen_datetime(snapshot)
    gen_snapshot_id(snapshot)
    if should_gen_user:
        gen_user(snapshot)
    gen_pose(snapshot.pose)
    gen_color_image_data(snapshot.color_image)
    gen_depth_image_data(snapshot.depth_image)
    gen_feelings(snapshot.feelings)
    align_protobuf(snapshot)
    return snapshot


def gen_snapshot_for_parsers(path, snapshot=None, should_gen_user=False):
    snapshot = snapshot or server_parsers_pb2.Snapshot()
    snapshot.datetime = gen_datetime()
    snapshot.uuid = gen_snapshot_id()
    if should_gen_user:
        gen_user(snapshot.user)
    snapshot_path = get_snapshot_path(snapshot, path)
    gen_pose(snapshot.pose)
    gen_color_image_raw(snapshot_path, snapshot.color_image)
    gen_depth_image_raw(snapshot_path, snapshot.depth_image)
    gen_feelings(snapshot.feelings)
    align_protobuf(snapshot)
    return snapshot


def gen_data_for_saver(path, num_users, num_snapshots):
    path = normalize_path(path)
    users_snapshots = {}
    all_results = []
    for i in range(num_users):
        user = gen_user()
        snapshots = []
        for j in range(num_snapshots):
            snapshot = {'datetime': gen_datetime(), 'uuid': gen_snapshot_id(), 'user': user, 'pose': gen_pose,
                        'feelings': gen_feelings()}
            snapshot_path = get_snapshot_path(snapshot, path, is_dict=True)
            snapshot['pose'] = gen_pose()
            snapshot['color_image'] = gen_color_image_parsed(snapshot_path)
            snapshot['depth_image'] = gen_depth_image_parsed(snapshot_path)
            snapshot['feelings'] = gen_feelings()
            snapshots.append(snapshot)
            results = dict_projection(snapshot, PARSERS)
            for key, value in results.items():
                all_results.append((key, {'uuid': snapshot['uuid'], 'datetime': snapshot['datetime'],
                                          'user': snapshot['user'], 'result': value}))
        users_snapshots[user['user_id']] = {'user': user, 'snapshots': snapshots}
    return all_results, users_snapshots


def gen_db_data(path, num_users, num_snapshots, database=None):
    path = normalize_path(path)
    _, users_snapshots = gen_data_for_saver(path, num_users, num_snapshots)
    db_data = []
    for user_id, entry in users_snapshots.items():
        db_entry = entry['user']
        db_entry['_id'] = db_entry['user_id'] = str(db_entry['user_id'])  # TODO: remove this workaround
        db_entry['snapshots'] = []
        for snapshot in entry['snapshots']:
            snapshot.pop('user')
            snapshot['_id'] = snapshot['uuid'] = str(snapshot['uuid'])  # TODO: remove this workaround
            snapshot['datetime'] = str(snapshot['datetime'])  # TODO: remove this workaround
            snapshot['results'] = {}
            for result in ['pose', 'color_image', 'depth_image', 'feelings']:
                if result in snapshot:
                    snapshot['results'][result] = snapshot.pop(result)
            db_entry['snapshots'].append(snapshot)
        db_data.append(db_entry)
    if database:
        coll = database[COLLECTION_NAME]
        coll.insert_many(db_data)
        return db_data, coll
    return db_data
