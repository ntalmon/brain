from PIL import Image


def parse_color_image(data):
    if 'color_image' not in data:
        return  # TODO: handle this case
    color_image = data['color_image']
    if 'width' not in color_image or 'height' not in color_image or 'path' not in color_image:
        return  # TODO: handle this case
    width, height, path = color_image['width'], color_image['height'], color_image['path']
    new_path = ''  # TODO: find new path
    with open(path, 'rb') as reader:
        data = reader.read()
    image = Image.frombytes('RGB', (width, height), data)
    image.save(new_path)
    return new_path


parse_color_image.field = 'color_image'
