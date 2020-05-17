import subprocess
import time

import coverage
import pytest

LOCALHOST = '127.0.0.1'
MQ_URL = 'rabbitmq://127.0.0.1:5672'
DB_URL = 'mongodb://127.0.0.1:27017'
SERVER_PORT = 8000


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


def test_end2end(services, random_sample):
    user, snapshots, file_path = random_sample
    proc_client = run_cmd(['python', '-m', 'brain.client', 'upload-sample', str(file_path)])
    stdout, stderr = proc_client.communicate()
    assert proc_client.returncode == 0, stderr
    assert b'All snapshots uploaded successfully' in stdout
    proc_client.terminate()


def test_thread2thread():
    pass
