from PIL import Image

from brain.utils.common import get_logger

logger = get_logger(__name__)


def parse_color_image(data, context):
    """
    Parse color image. Constructing the data from the raw file, and then saving it as image in jpg format.
    After generating the jpg image, we don't need the raw file anymore, so delete it.

    :param data: a dictionary that contains `width`, `height`, and `file_name`
    :param context: the context object.
    :return: a dictionary width the given width and height, and full path to the generated jpg file.
    """

    logger.info(f'running color_image parser')
    width, height, file_name = data['width'], data['height'], data['file_name']
    path = context.path(file_name)
    new_path = context.path('color_image.jpg')
    # read raw color image file
    with open(path, 'rb') as reader:
        color_image = reader.read()
    # parse and save to JPEG
    image = Image.frombytes('RGB', (width, height), color_image)
    image.save(new_path)
    # delete old file
    context.delete(file_name)
    return {'width': width, 'height': height, 'path': new_path}


parse_color_image.field = 'color_image'
