import os
import random

first_names = ('John', 'Andy', 'Joe')
last_names = ('Johnson', 'Smith', 'Williams')


def gen_random_user():
    return {
        'user_id': random.randint(0, 100),
        'username': f'{random.choice(first_names)} {random.choice(last_names)}',
        'birthday': random.getrandbits(32),
        'gender': random.randint(0, 2)
    }


def gen_pose():
    return {
        'translation': {
            'x': float(random.uniform(-100, 100)),
            'y': float(random.uniform(-100, 100)),
            'z': float(random.uniform(-100, 100))
        },
        'rotation': {
            'x': float(random.uniform(-100, 100)),
            'y': float(random.uniform(-100, 100)),
            'z': float(random.uniform(-100, 100)),
            'w': float(random.uniform(-100, 100))
        }
    }


def gen_color_image():
    width = random.randint(5, 10)
    height = random.randint(5, 10)
    return {
        'width': width,
        'height': height,
        'data': os.urandom(width * height * 3)
    }


def gen_depth_image():
    width = random.randint(5, 10)
    height = random.randint(5, 10)
    return {
        'width': width,
        'height': height,
        'data': [float(random.uniform(-100, 100)) for _ in range(width * height)]
    }


def gen_feelings():
    return {
        'hunger': float(random.uniform(-1, 1)),
        'thirst': float(random.uniform(-1, 1)),
        'exhaustion': float(random.uniform(-1, 1)),
        'happiness': float(random.uniform(-1, 1))
    }


def gen_random_snapshot():
    return {
        'pose': gen_pose(),
        'color_image': gen_color_image(),
        'depth_image': gen_depth_image(),
        'feelings': gen_feelings()
    }
