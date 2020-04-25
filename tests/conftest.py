import random
import pytest

from brain import tests_path as _tests_path
from brain.autogen import reader_pb2

_resources_path = _tests_path / 'resources'
first_names = ('John', 'Andy', 'Joe')
last_names = ('Johnson', 'Smith', 'Williams')


@pytest.fixture(scope='session')
def tests_path():
    return _tests_path


@pytest.fixture(scope='session')
def resources_path():
    return _resources_path


def _gen_random_user_name():
    return f'{random.choice(first_names)} {random.choice(last_names)}'


@pytest.fixture
def random_user():
    user = reader_pb2.User()
    user.user_id = random.randint(1, 100)
    user.user_name = _gen_random_user_name()
    user.birthday = random.getrandbits(32)
    user.gender = random.choice(reader_pb2.User.Gender.values())
    return user
