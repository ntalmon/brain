import subprocess
import time
from functools import partial

import coverage
import pytest

from brain.utils.consts import *
from .utils import cli_run_and_check, run_flask_in_thread


def run_cmd(cmd):
    coverage.process_startup()
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    return process


@pytest.fixture
def services():
    processes = {'server': run_cmd(['python', '-m', 'brain.server', 'run-server', MQ_URL]),
                 'pose': run_cmd(['python', '-m', 'brain.parsers', 'run-parser', 'pose', MQ_URL]),
                 'color_image': run_cmd(['python', '-m', 'brain.parsers', 'run-parser', 'color_image', MQ_URL]),
                 'depth_image': run_cmd(['python', '-m', 'brain.parsers', 'run-parser', 'depth_image', MQ_URL]),
                 'feelings': run_cmd(['python', '-m', 'brain.parsers', 'run-parser', 'feelings', MQ_URL]),
                 'saver': run_cmd(['python', '-m', 'brain.saver', 'run-saver', DB_URL, MQ_URL]),
                 'api': run_cmd(['python', '-m', 'brain.api', 'run-server'])}
    time.sleep(5)  # TODO: find more elegant way to make sure services are up
    yield processes
    for process in processes.values():
        assert process.poll() is None  # make sure service is still up
        process.terminate()


@pytest.mark.skip()
def test_end2end(services, random_sample):
    user, snapshots, file_path = random_sample
    proc_client = run_cmd(['python', '-m', 'brain.client', 'upload-sample', str(file_path)])
    stdout, stderr = proc_client.communicate()
    assert proc_client.returncode == 0, stderr
    assert b'All snapshots uploaded successfully' in stdout
    proc_client.terminate()


@pytest.fixture
def server_thread():
    from brain.server.__main__ import cli
    from brain.server.client_agent import app
    callback = partial(cli_run_and_check, cli, ['run-server', MQ_URL])
    # TODO: handle server url
    yield from run_flask_in_thread(app, 'http://127.0.0.1:8000', callback)
