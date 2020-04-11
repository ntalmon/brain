def parse_pose(data):
    if 'pose' not in data:
        return None  # TODO: handle this case
    pose = data['pose']
    return pose


parse_pose.field = 'pose'
