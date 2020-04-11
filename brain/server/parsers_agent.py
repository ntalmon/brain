import numpy as np


def handle_color_image(snapshot_dict, snapshot_dir):
    data = snapshot_dict['color_image']['data']
    image_file = snapshot_dir / 'color_image.raw'
    with open(str(image_file), 'wb') as write:
        write.write(data)
    del snapshot_dict['color_image']['data']
    snapshot_dict['color_image']['path'] = str(image_file)


def handle_depth_image(snapshot_dict, snapshot_dir):
    data = snapshot_dict['depth_image']['data']
    image_file = snapshot_dir / 'depth_image.raw'
    array = np.array(data).astype(np.float)
    np.save(str(image_file), array)
    del snapshot_dict['depth_image']['data']
    snapshot_dict['depth_image']['path'] = str(image_file)


def construct_json(snapshot):
    """
    TODO: move to protobuf
    """
    snapshot_dict = json_format.MessageToDict(snapshot)
    user_id = snapshot_dict['user']['user_id']
    user_dir = data_path / str(user_id)
    if not user_dir.exists():
        user_dir.mkdir()
    timestamp = snapshot_dict['datetime']
    snapshot_dir = user_dir / str(timestamp)
    snapshot_dir.mkdir()
    if 'color_image' in snapshot_dict:
        handle_color_image(snapshot_dict, snapshot_dir)
    if 'depth_image' in snapshot_dict:
        handle_depth_image(snapshot_dict, snapshot_dir)
    return json.dumps(snapshot_dict)
