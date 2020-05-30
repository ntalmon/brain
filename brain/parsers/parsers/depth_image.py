import matplotlib.pyplot as plt
import numpy as np

from brain.utils.common import get_logger

logger = get_logger(__name__)


def parse_depth_image(data, context):
    """
    Parse depth image. Constructing the data from the raw file, and then saving it as image in jpg format.
    After generating the jpg image, we don't need the raw file anymore, so delete it.

    :param data: a dictionary that contains `width`, `height`, and `file_name`
    :param context: the context object.
    :return: a dictionary width the given width and height, and full path to the generated jpg file.
    """

    logger.info(f'running depth_image parser')
    width, height, file_name = data['width'], data['height'], data['file_name']
    path = context.path(file_name)
    new_path = context.path('depth_image.jpg')
    # read raw depth image
    array = np.load(path).reshape((height, width))
    # parse and save to JPEG
    plt.imshow(array)
    plt.savefig(new_path)
    # delete old file
    context.delete(file_name)
    return {'width': width, 'height': height, 'path': new_path}


parse_depth_image.field = 'depth_image'
