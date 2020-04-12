"""
TODO: send context to parsers if needed
"""
import importlib
import json
import sys

from google.protobuf import json_format

from brain import brain_path
from brain.autogen import parsers_pb2
from brain.mq import MQAgent

parsers = {}
parsers_path = brain_path / 'parsers'


def _wrap_parser(parse_fn):
    def _wrapper(data):
        # TODO: currently assume snapshot is protobuf, maybe change it
        snapshot = parsers_pb2.Snapshot()
        snapshot.ParseFromString(data)
        json_snapshot = json_format.MessageToDict(snapshot, including_default_value_fields=True,
                                                  preserving_proto_field_name=True)
        res = parse_fn(json_snapshot)
        res = {
            'uuid': json_snapshot['uuid'],
            'datetime': json_snapshot['datetime'],
            'user': json_snapshot['user'],
            'result': res
        }
        return res

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
    def __init__(self):
        pass

    def save(self, file, data):
        pass

    def path(self, file):
        pass


def parser(tag):
    def decorator(f):
        parsers[tag] = f
        return f

    return decorator


def run_parser(tag, data):  # TODO: rename tag variable
    if tag not in parsers:
        return None  # TODO: handle this case
    return parsers[tag](data)


def invoke_parser(tag, url):
    if tag not in parsers:
        return  # TODO: handle this case
    _parser = parsers[tag]
    mq_agent = MQAgent(url)

    def callback(body):
        snapshot = parsers_pb2.Snapshot()
        snapshot.ParseFromString(body)
        # body = json_format.MessageToDict(snapshot)  # TODO: get rid of the json if possible (parsers will get protobuf)
        res = _parser(body)  # TODO: change res format if needed
        res = json.dumps(res)
        mq_agent.publish(res, queue=f'saver_{tag}')  # TODO: find right exchange and queue

    mq_agent.consume(callback, exchange='snapshot', queue=tag)
