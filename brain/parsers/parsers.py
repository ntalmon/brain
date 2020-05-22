import importlib
import inspect
import json
import os
import pathlib
import sys

from google.protobuf import json_format

from brain import brain_path
from brain.autogen import server_parsers_pb2
from .mq_agent import MQAgent

parsers = {}
parsers_path = brain_path / 'parsers'


def load_parsers():
    sys.path.insert(0, str(parsers_path.parent))
    for path in parsers_path.iterdir():
        if path.name.startswith('_') or path.suffix != '.py' or path.name == 'parsers.py':
            continue
        module = importlib.import_module(f'{parsers_path.name}.{path.stem}')
        for name, obj in module.__dict__.items():
            if callable(obj) and name.startswith('parse_') and hasattr(obj, 'field'):
                obj.parser_type = 'function'
                parsers[obj.field] = obj
            elif inspect.isclass(obj) and name.lower().endswith('parser') and hasattr(obj, 'parse') and \
                    hasattr(obj, 'field'):
                instance = obj()
                instance.parser_type = 'class'
                parsers[obj.field] = instance


load_parsers()


def get_parsers():
    return parsers.keys()


class Context:
    def __init__(self, path=''):
        if path and isinstance(path, str):
            path = pathlib.Path(path)
        self.base_path = path

    def save(self, file, data):
        if not self.base_path:
            raise Exception('Cannot access context.path when save is not initialized')
        mode = 'w' + 'b' * isinstance(data, bytes)
        with open(self.path(file), mode) as writer:
            writer.write(data)

    def path(self, file):
        if not self.base_path:
            raise Exception('Cannot access context.path when save is not initialized')
        return str(self.base_path / file)

    def delete(self, file):
        if not self.base_path:
            raise Exception('Cannot access context.delete when save is not initialized')
        os.remove(self.path(file))


def parser_wrapper(parse_fn, data):
    snapshot = server_parsers_pb2.Snapshot()
    snapshot.ParseFromString(data)
    json_snapshot = json_format.MessageToDict(
        snapshot, including_default_value_fields=True, preserving_proto_field_name=True)
    field = parse_fn.field
    if parse_fn.parser_type == 'class':
        parse_fn = parse_fn.parse
    parser_data = json_snapshot[field]
    path = json_snapshot['path']
    ctx = Context(path)

    parse_res = parse_fn(parser_data, ctx)
    res = {
        'uuid': json_snapshot['uuid'],
        'datetime': json_snapshot['datetime'],
        'user': json_snapshot['user'],
        'result': parse_res
    }
    return res


def parser(topic):
    def decorator(f):
        parsers[topic] = f
        return f

    return decorator


def run_parser(parser_name, data, is_path=False):
    if parser_name not in parsers:
        raise Exception(f'Could not find given parser name \'{parser_name}\'')
    if is_path:
        with open(data, 'rb') as file:
            data = file.read()
    parse_fn = parsers[parser_name]
    return parser_wrapper(parse_fn, data)


def invoke_parser(topic, url):
    if topic not in parsers:
        raise Exception(f'Parser not found: {topic}')
    _parser = parsers[topic]
    mq_agent = MQAgent(url)

    def callback(body):
        snapshot = server_parsers_pb2.Snapshot()
        snapshot.ParseFromString(body)
        res = parser_wrapper(_parser, body)
        parse_res_msg = json.dumps(res)
        mq_agent.publish_result(parse_res_msg, topic)

    mq_agent.consume_snapshots(callback, topic)
