import pytest

from brain import tests_path as _tests_path

_resources_path = _tests_path / 'resources'


@pytest.fixture(scope='session')
def tests_path():
    return _tests_path


@pytest.fixture(scope='session')
def resources_path():
    return _resources_path
