from PIL import Image


def parse_color_image(data, context):  # TODO: after writing parsed file, delete raw file
    if 'width' not in data or 'height' not in data or 'file_name' not in data:
        return  # TODO: handle this case
    width, height, file_name = data['width'], data['height'], data['file_name']
    path = context.path(file_name)
    new_path = context.path('color_image.jpg')
    with open(path, 'rb') as reader:
        color_image = reader.read()
    image = Image.frombytes('RGB', (width, height), color_image)
    image.save(new_path)
    return {'width': width, 'height': height, 'path': new_path}


parse_color_image.field = 'color_image'
