from brain.utils.common import get_logger

logger = get_logger(__name__)


def parse_pose(data, context):
    logger.info(f'running pose parser')
    return data


parse_pose.field = 'pose'
