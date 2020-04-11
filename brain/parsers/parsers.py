"""
TODO: send context to parsers if needed
"""
import importlib
import json
import pathlib
import sys

from brain.mq import MQAgent

parsers = {}
parsers_path = pathlib.Path(__file__).parent.absolute()


def get_parsers():
    return parsers.keys()


def load_parsers():
    sys.path.insert(0, str(parsers_path.parent))
    for path in parsers_path.iterdir():
        if path.name.startswith('_') or path.suffix != '.py' or path.name == 'parsers.py':
            continue
        module = importlib.import_module(f'{parsers_path.name}.{path.stem}')
        for name, obj in module.__dict__.items():
            if callable(obj) and name.startswith('parse_') and hasattr(obj, 'field'):
                parsers[obj.field] = obj


load_parsers()


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
        body = json.loads(body)  # TODO: should we handle json format anywhere else?
        res = _parser(body)  # TODO: change res format if needed
        res = json.dumps(res)
        mq_agent.publish(res)  # TODO: find right exchange and queue

    mq_agent.consume(callback, exchange='snapshot')
