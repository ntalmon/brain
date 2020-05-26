import pytest
import requests
from click.testing import CliRunner

import brain.gui.gui
from brain.gui.__main__ import cli
from brain.gui.gui import app
from brain.gui.gui import run_server
from brain.utils.consts import *
from .utils import run_flask_in_thread


def simple_get_index():
    res = requests.get(f'{GUI_URL}')
    assert res.status_code == 200
    assert 'text/html' in res.headers['Content-Type']
    assert res.text.startswith('<!doctype html>')


def simple_get_resource():
    res = requests.get(f'{GUI_URL}/brain.png')
    assert res.status_code == 200
    assert 'image/png' in res.headers['Content-Type']


@pytest.fixture
def run_gui_in_thread():
    yield from run_flask_in_thread(app, GUI_URL, lambda: run_server(GUI_HOST, GUI_PORT, API_HOST, API_PORT))


def test_run_server(run_gui_in_thread):
    poll_exc = run_gui_in_thread
    poll_exc()
    simple_get_index()
    poll_exc()
    simple_get_resource()
    poll_exc()


@pytest.fixture
def mock_flask(monkeypatch):
    def fake_render_template(*args, **kwargs):
        raise Exception('Expected exception from fake_render_template')

    monkeypatch.setattr(brain.gui.gui.flask, 'render_template', fake_render_template)


def test_exception(mock_flask, capsys):
    with app.test_client() as client:
        res = client.get('/')
        assert res.status_code == 500
        # out, err = capsys.readouterr()
        # assert 'Expected exception from fake_render_template' in out


@pytest.fixture
def run_cli_in_thread():
    def callback():
        runner = CliRunner()
        res = runner.invoke(cli, ['run-server'])
        assert res.exception == 0

    from brain.gui.gui import app
    yield from run_flask_in_thread(app, GUI_URL, callback)


def test_cli(run_cli_in_thread):
    poll_exc = run_cli_in_thread
    poll_exc()
    simple_get_index()
    poll_exc()
    simple_get_resource()
    poll_exc()
