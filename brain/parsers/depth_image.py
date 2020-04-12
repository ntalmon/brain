import matplotlib.pyplot as plt
import numpy as np
import pathlib


def parse_depth_image(data):  # TODO: after writing parsed file, delete raw file
    if 'depth_image' not in data:
        return  # TODO: handle this case
    depth_image = data['depth_image']
    if 'width' not in depth_image or 'height' not in depth_image or 'path' not in depth_image:
        return  # TODO: handle this case
    width, height, path = depth_image['width'], depth_image['height'], depth_image['path']
    new_path = str(pathlib.Path(path).parent / 'depth_image.jpg')  # TODO: is it OK to save in the saver directory?
    array = np.load(path).reshape((width, height))
    plt.imshow(array)
    plt.savefig(new_path)
    return new_path


parse_depth_image.field = 'depth_image'
