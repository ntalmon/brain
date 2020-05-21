import pathlib

import numpy as np

from brain import data_path
from brain.autogen import server_parsers_pb2


def copy_protobuf(item_a, item_b, attrs):
    for attr in attrs:
        setattr(item_a, attr, getattr(item_b, attr))


def handle_color_image(snapshot, data):
    path = pathlib.Path(snapshot.path)
    image_file = str(path / 'color_image.raw')
    with open(image_file, 'wb') as writer:
        writer.write(data)
    snapshot.color_image.file_name = image_file


def handle_depth_image(snapshot, data):
    path = pathlib.Path(snapshot.path)
    image_file = 'depth_image.raw'
    image_file_path = str(path / image_file)
    array = np.array(data).astype(np.float)
    np.save(image_file_path, array)
    snapshot.depth_image.file_name = image_file + '.npy'


def construct_parsers_message(snapshot, snapshot_uuid):
    parsers_snapshot = server_parsers_pb2.Snapshot()
    parsers_snapshot.uuid = snapshot_uuid
    copy_protobuf(parsers_snapshot, snapshot, ['datetime'])
    copy_protobuf(parsers_snapshot.user, snapshot.user, ['user_id', 'username', 'birthday', 'gender'])
    copy_protobuf(parsers_snapshot.pose.translation, snapshot.pose.translation, ['x', 'y', 'z'])
    copy_protobuf(parsers_snapshot.pose.rotation, snapshot.pose.rotation, ['x', 'y', 'z', 'w'])
    copy_protobuf(parsers_snapshot.color_image, snapshot.color_image, ['width', 'height'])
    copy_protobuf(parsers_snapshot.depth_image, snapshot.depth_image, ['width', 'height'])
    copy_protobuf(parsers_snapshot.feelings, snapshot.feelings, ['hunger', 'thirst', 'exhaustion', 'happiness'])

    user_id = parsers_snapshot.user.user_id
    user_dir = data_path / str(user_id)
    if not user_dir.exists():
        user_dir.mkdir()
    snapshot_dir = user_dir / str(parsers_snapshot.uuid)
    if not snapshot_dir.exists():
        snapshot_dir.mkdir()
    parsers_snapshot.path = str(snapshot_dir)

    if snapshot.color_image:
        handle_color_image(parsers_snapshot, snapshot.color_image.data)
    if parsers_snapshot.depth_image:
        handle_depth_image(parsers_snapshot, snapshot.depth_image.data)
    return parsers_snapshot.SerializeToString()
