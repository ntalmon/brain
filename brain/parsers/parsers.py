import importlib
import inspect
import json
import os
import pathlib
import sys

from google.protobuf import json_format

from brain import brain_path
from brain.autogen import server_parsers_pb2
from brain.utils.common import normalize_path, get_logger
from .mq_agent import MQAgent

logger = get_logger(__name__)
parsers = {}
parsers_path = brain_path / 'parsers'


def load_parsers():
    logger.info(f'loading parsers')
    sys.path.insert(0, str(parsers_path.parent))
    for path in parsers_path.iterdir():
        if path.name.startswith('_') or path.suffix != '.py' or path.name == 'parsers.py':
            continue
        module = importlib.import_module(f'{parsers_path.name}.{path.stem}')
        for name, obj in module.__dict__.items():
            if callable(obj) and name.startswith('parse_') and hasattr(obj, 'field'):
                logger.info(f'found function parser {name} in {module.__name__}')
                obj.parser_type = 'function'
                parsers[obj.field] = obj
            elif inspect.isclass(obj) and name.lower().endswith('parser') and hasattr(obj, 'parse') and \
                    hasattr(obj, 'field'):
                logger.info(f'found class parser {name} in {module.__name__}')
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
            logger.error(f'trying to access context.save but path is not initializing')
            raise Exception('Cannot access context.path when save is not initialized')
        mode = 'w' + 'b' * isinstance(data, bytes)
        with open(self.path(file), mode) as writer:
            writer.write(data)

    def path(self, file):
        if not self.base_path:
            logger.error(f'trying to access context.path but path is not initializing')
            raise Exception('Cannot access context.path when save is not initialized')
        return str(self.base_path / file)

    def delete(self, file):
        if not self.base_path:
            logger.error(f'trying to access context.delete but path is not initializing')
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
    path = normalize_path(snapshot.path)
    ctx = Context(path)

    parse_res = parse_fn(parser_data, ctx)
    res = {
        'uuid': json_snapshot['uuid'],
        'datetime': json_snapshot['datetime'],
        'user': json_snapshot['user'],
        'result': parse_res
    }
    return res


def run_parser(parser_name, data, is_path=False):
    if parser_name not in parsers:
        raise Exception(f'Could not find given parser name \'{parser_name}\'')
    logger.info(f'running parser {parser_name}')
    if is_path:
        with open(data, 'rb') as file:
            data = file.read()
    parse_fn = parsers[parser_name]
    return parser_wrapper(parse_fn, data)


def invoke_parser(topic, url):
    if topic not in parsers:
        logger.error(f'topic {topic} was not found in parsers')
        raise Exception(f'Parser not found: {topic}')
    _parser = parsers[topic]
    mq_agent = MQAgent(url)

    def callback(body):
        snapshot = server_parsers_pb2.Snapshot()
        snapshot.ParseFromString(body)
        logger.debug(f'calling parser {topic}')
        res = parser_wrapper(_parser, body)
        parse_res_msg = json.dumps(res)
        logger.debug(f'publish result to message queue')
        mq_agent.publish_result(parse_res_msg, topic)

    logger.info(f'starting to consume mq: {topic=}')
    mq_agent.consume_snapshots(callback, topic)
