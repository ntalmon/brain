from brain.utils.common import get_logger

logger = get_logger(__name__)


def parse_pose(data, context):
    """
    Parsing pose. Currently there is no what to parse, as the data is already in the right format.

    :param data: dictionary containing the pose as appears in the snapshot.
    :param context: given by the parsers framework.
    :return: the given data.
    """

    logger.info(f'running pose parser')
    return data


parse_pose.field = 'pose'
