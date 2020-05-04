import pytest
from brain.saver import Saver

DB_URL = 'mongodb://127.0.0.1:27017'


@pytest.fixture
def saver():
    return Saver(DB_URL)


def test_save(saver):
    assert False


def test_run_saver():
    assert False


def test_mq_agent():
    assert False


def test_db_agent():
    assert False


def test_cli():
    assert False
