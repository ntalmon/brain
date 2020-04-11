import pathlib

import pytest

_tests_path = pathlib.Path(__file__).parent.absolute()
_resources_path = _tests_path / 'resources'


@pytest.fixture(scope='session')
def tests_path():
    return _tests_path


@pytest.fixture(scope='session')
def resources_path():
    return _resources_path
