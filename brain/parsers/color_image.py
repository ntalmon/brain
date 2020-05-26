from PIL import Image

from brain.utils.common import get_logger

logger = get_logger(__name__)


def parse_color_image(data, context):
    logger.info(f'running color_image parser')
    width, height, file_name = data['width'], data['height'], data['file_name']
    path = context.path(file_name)
    new_path = context.path('color_image.jpg')
    with open(path, 'rb') as reader:
        color_image = reader.read()
    image = Image.frombytes('RGB', (width, height), color_image)
    image.save(new_path)
    context.delete(file_name)
    return {'width': width, 'height': height, 'path': new_path}


parse_color_image.field = 'color_image'
