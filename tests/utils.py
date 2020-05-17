import multiprocessing
import socket
import subprocess
import threading
import time

import flask
import requests
from furl import furl
from google.protobuf import json_format


def execute_command(command, safety=False):
    sp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    code, out, err = sp.returncode, sp.stdout.read(), sp.stderr.read()
    if safety:
        assert code == 0, f'Error while executing command: command={command}, exit-code={code}'
    return code, out, err


def protobuf2dict(x):
    return json_format.MessageToDict(x, including_default_value_fields=True, preserving_proto_field_name=True)


def cmp_protobuf(x, y):
    dict_x = protobuf2dict(x)
    dict_y = protobuf2dict(y)
    return dict_x == dict_y


def json2pb(js_dict, pb_obj, serialize=False):
    def recursion(_js_dict, _pb_obj):
        for key, value in _js_dict.items():
            if isinstance(value, dict):
                recursion(value, getattr(_pb_obj, key))
            elif isinstance(value, list):
                getattr(_pb_obj, key)[:] = value
            else:
                setattr(_pb_obj, key, value)

    recursion(js_dict, pb_obj)
    pb_str = pb_obj.SerializeToString()
    if serialize:
        return pb_str
    pb_obj.ParseFromString(pb_str)
    return pb_obj


def run_process(runner):
    parent, child = multiprocessing.Pipe()

    process = multiprocessing.Process(target=runner, args=(child,))
    process.start()
    parent.recv()
    try:
        yield lambda: parent.recv()
    finally:
        process.terminate()
        process.join()


def dict_projection(d, items):
    return {key: value for key, value in d.items() if key in items}


def run_in_background(callback, poll=1):
    try:
        from pytest_cov.embed import cleanup_on_sigterm
    except ImportError:
        pass
    else:
        cleanup_on_sigterm()

    parent, child = multiprocessing.Pipe()
    process = multiprocessing.Process(target=callback, args=(child,))
    process.start()
    parent.recv()
    try:
        def get_message():
            if not parent.poll(poll):
                raise TimeoutError()
            return parent.recv()

        yield get_message
    finally:
        process.terminate()
        process.join()


def shutdown_server(url):
    shutdown_url = str(furl(url) / 'shutdown')
    requests.post(shutdown_url)


def add_shutdown_to_app(app):
    if hasattr(app, 'has_shutdown') and app.has_shutdown:
        return

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        func = flask.request.environ.get('werkzeug.server.shutdown')
        if func is None:
            raise RuntimeError('Not running with the Werkzeug Server')
        func()

    app.has_shutdown = True


def wait_for_address(host, port, timeout=5.0):
    start_time = time.perf_counter()
    while True:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                break
        except OSError as ex:
            time.sleep(0.01)
            if time.perf_counter() - start_time >= timeout:
                raise TimeoutError('Waited too long for the port {} on host {} to start accepting '
                                   'connections.'.format(port, host)) from ex


def run_flask_in_thread(app, url, callback):
    add_shutdown_to_app(app)
    exc = None  # type: Exception

    def wrapper():  # TODO: move this procedure to common utils?
        try:
            callback()
        except Exception as error:
            nonlocal exc
            exc = error

    def poll_exc():
        if exc:
            raise exc

    thr = threading.Thread(target=wrapper)
    thr.start()
    url_obj = furl(url)
    host, port = url_obj.host, url_obj.port
    wait_for_address(host, port)
    yield poll_exc
    shutdown_server(url)
    poll_exc()
    thr.join(timeout=10)
