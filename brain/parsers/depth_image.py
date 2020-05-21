import matplotlib.pyplot as plt
import numpy as np


def parse_depth_image(data, context):
    width, height, file_name = data['width'], data['height'], data['file_name']
    path = context.path(file_name)
    new_path = context.path('depth_image.jpg')
    array = np.load(path).reshape((height, width))
    plt.imshow(array)
    plt.savefig(new_path)
    context.delete(file_name)
    return {'width': width, 'height': height, 'path': new_path}


parse_depth_image.field = 'depth_image'
