"""
TODO: send context to parsers if needed
"""
import importlib
import json
import pathlib
import sys

from google.protobuf import json_format

from .mq_agent import MQAgent
from brain import brain_path
from brain.autogen import parsers_pb2

parsers = {}
parsers_path = brain_path / 'parsers'


def _wrap_parser(parse_fn):
    def _wrapper(data):
        # TODO: currently assume snapshot is protobuf, maybe change it
        snapshot = parsers_pb2.Snapshot()
        snapshot.ParseFromString(data)
        json_snapshot = json_format.MessageToDict(
            snapshot, including_default_value_fields=True, preserving_proto_field_name=True)
        parse_res = parse_fn(json_snapshot)
        res = {
            'uuid': json_snapshot['uuid'],
            'datetime': json_snapshot['datetime'],
            'user': json_snapshot['user'],
            'result': parse_res
        }
        return res  # TODO: json.dumps?

    return _wrapper


def load_parsers():
    sys.path.insert(0, str(parsers_path.parent))
    for path in parsers_path.iterdir():
        if path.name.startswith('_') or path.suffix != '.py' or path.name == 'parsers.py':
            continue
        module = importlib.import_module(f'{parsers_path.name}.{path.stem}')
        for name, obj in module.__dict__.items():
            if callable(obj) and name.startswith('parse_') and hasattr(obj, 'field'):
                parsers[obj.field] = _wrap_parser(obj)


load_parsers()


def get_parsers():
    return parsers.keys()


class Context:
    def __init__(self, path):
        self.color_image_raw = str(path / 'color_image_raw')

    def save(self, file, data):
        pass

    def path(self, file):
        pass


def parser(topic):
    def decorator(f):
        parsers[topic] = f
        return f

    return decorator


# TODO: check if it is ok to add these additional parameters
def run_parser(parser_name, data, is_path=False):
    if parser_name not in parsers:
        raise Exception(f'Could not find given parser name \'{parser_name}\'')
    if is_path:
        with open(data, 'rb') as file:
            data = file.read()
    return parsers[parser_name](data)


def invoke_parser(topic, url):
    if topic not in parsers:
        return  # TODO: handle this case
    _parser = parsers[topic]
    mq_agent = MQAgent(url)

    def callback(body):
        snapshot = parsers_pb2.Snapshot()
        snapshot.ParseFromString(body)
        res = _parser(body)  # TODO: change res format if needed
        parse_res_msg = json.dumps(res)
        mq_agent.publish_result(parse_res_msg, topic)

    mq_agent.consume_snapshots(callback, topic)
