"""
TODO: move to aspect-oriented programming
"""
from brain.mq import MQAgent

parsers = {}


def parser(tag):
    def decorator(f):
        parsers[tag] = f
        return f

    return decorator


class Context:
    def __init__(self):
        pass


def run_parser(tag, data):
    if tag not in parsers:
        return None  # TODO: handle this case
    ctx = Context()  # TODO: handle context
    return parsers[tag](ctx, data)


def invoke_parser(tag, url):
    if tag not in parsers:
        return  # TODO: handle this case
    _parser = parsers[tag]
    ctx = Context()  # TODO: handle context
    mq_agent = MQAgent(url)

    def callback(body):
        res = _parser(ctx, body)  # TODO: change res format if needed
        mq_agent.publish(res)  # TODO: find right exchange and queue

    mq_agent.consume(callback, exchange='snapshot')
