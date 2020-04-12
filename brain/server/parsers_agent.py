import numpy as np

from brain import data_path
from brain.autogen import parsers_pb2


def copy_protobuf(item_a, item_b, attrs):
    for attr in attrs:
        setattr(item_a, attr, getattr(item_b, attr))


def handle_color_image(snapshot, data, snapshot_dir):
    image_file = snapshot_dir / 'color_image.raw'
    with open(str(image_file), 'wb') as write:
        write.write(data)

    snapshot.color_image.path = str(image_file)


def handle_depth_image(snapshot, data, snapshot_dir):
    image_file = snapshot_dir / 'depth_image.raw'
    array = np.array(data).astype(np.float)
    np.save(str(image_file), array)
    snapshot.depth_image.path = str(image_file)


def construct_parsers_message(snapshot):
    parsers_snapshot = parsers_pb2.Snapshot()
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
    timestamp = parsers_snapshot.datetime
    snapshot_dir = user_dir / str(timestamp)
    if not snapshot_dir.exists():
        snapshot_dir.mkdir()
    if snapshot.color_image:
        handle_color_image(parsers_snapshot, snapshot.color_image.data, snapshot_dir)
    if parsers_snapshot.depth_image:
        handle_depth_image(parsers_snapshot, snapshot.depth_image.data, snapshot_dir)
    return parsers_snapshot.SerializeToString()
