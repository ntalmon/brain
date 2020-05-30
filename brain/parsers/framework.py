"""
The framework module contains the parsers framework, which including parsers detection, running and invocation.
"""

import importlib
import inspect
import os
import pathlib
import sys
from typing import Union

from brain import brain_path
from brain.autogen import server_parsers_pb2
from brain.utils.common import normalize_path, get_logger, protobuf2dict, parse_protobuf, get_url_scheme
from .mq_agent import load_mq_agent

# from ..utils.consts import

logger = get_logger(__name__)
parsers = {}
parsers_path = brain_path / 'parsers' / 'parsers'


def load_parsers():
    """
    Loads all the parsers in the parsers subpackage.
    Looks for all files in the package and identifies a parser in one of the following ways:

    - Function starts with `parse_` (e.g. `parse_pose`) that has `field` attribute.
    - Class end with `Parser` (e.g. `FeelingsParser`) that has `field` member and parse method.
    """

    logger.info(f'loading parsers')
    sys.path.insert(0, str(parsers_path.parent))
    for path in parsers_path.iterdir():
        if path.name.startswith('_') or path.suffix != '.py' or path.name == 'framework.py':
            continue
        module = importlib.import_module(f'{parsers_path.name}.{path.stem}')
        for name, obj in module.__dict__.items():
            if callable(obj) and name.startswith('parse_') and hasattr(obj, 'field'):
                logger.info(f'found function parser {name} in {module.__name__}')
                parsers[obj.field] = obj
            elif inspect.isclass(obj) and name.lower().endswith('parser') and hasattr(obj, 'parse') and \
                    hasattr(obj, 'field'):
                logger.info(f'found class parser {name} in {module.__name__}')
                instance = obj()
                parsers[obj.field] = instance.parse


load_parsers()


def get_parsers() -> list:
    """
    Get the names of all the identified parsers.

    :return: list of parsers names.
    """

    return list(parsers.keys())


def get_parser_by_name(parser):
    try:
        return parsers[parser]
    except KeyError:
        logger.error(f'unsupported parser: {parser}')
        raise NotImplementedError(f'Unsupported parser: {parser}')


class Context:
    """
    The context class provide a context for accessing paths. An instance is passed to all the parsers and allows them
    to save, get and delete paths relatively to a predefined path given by the caller.

    :param path: if given, it will be the "base path" of the instance - accessing files via the context instance will
        be relatively to the base path.
    """

    def __init__(self, path: str = ''):
        if path and isinstance(path, str):
            path = pathlib.Path(path)
        self.base_path = path

    def save(self, file: str, data: Union[str, bytes]):
        """
        Write data to a file relatively to the base path.

        :param file: relative path (including file name).
        :param data: data to write to the file.
        """

        if not self.base_path:
            logger.error(f'trying to access context.save but path is not initializing')
            raise Exception('Cannot access context.path when save is not initialized')
        mode = 'w' + 'b' * isinstance(data, bytes)
        with open(self.path(file), mode) as writer:
            writer.write(data)

    def path(self, file: str) -> str:
        """
        Given a relative path, provide the full path including the base path.

        :param file: relative path.
        :return: the full path.
        """

        if not self.base_path:
            logger.error(f'trying to access context.path but path is not initializing')
            raise Exception('Cannot access context.path when save is not initialized')
        return str(self.base_path / file)

    def delete(self, file: str):
        """
        Delete a file.

        :param file: relative path to the file we want to delete.
        """

        if not self.base_path:
            logger.error(f'trying to access context.delete but path is not initializing')
            raise Exception('Cannot access context.delete when save is not initialized')
        os.remove(self.path(file))


def run_parser(parser_name: str, data: Union[str, bytes], is_path: bool = False) -> dict:
    """
    Run the parser with the given data.

    :param parser_name: parser to run.
    :param data: data for the parser or path to the file containing the data.
    :param is_path: is the `data` parameter contains the raw data or path?
    :return: the parser result.
    """
    if is_path:
        with open(data, 'rb') as file:
            data = file.read()

    logger.info(f'running parser {parser_name}')
    parse_fn = get_parser_by_name(parser_name)
    snapshot = parse_protobuf(server_parsers_pb2.Snapshot(), data)
    dict_snapshot = protobuf2dict(snapshot)
    parser_data = dict_snapshot[parser_name]
    path = normalize_path(snapshot.path)
    ctx = Context(path)
    parse_res = parse_fn(parser_data, ctx)
    return {
        'uuid': dict_snapshot['uuid'],
        'datetime': dict_snapshot['datetime'],
        'user': dict_snapshot['user'],
        'result': parse_res
    }


def invoke_parser(parser: str, mq_url: str):
    """
    Run the parser as a service, that consumes messages and publishes results using the given MQ.

    :param parser: name of the parser.
    :param mq_url: address of the MQ to consume and publish.
    """

    def callback(body):
        logger.debug(f'calling parser {parser}')
        res = run_parser(parser, body)  # run the parser
        logger.debug(f'publish result to message queue')
        mq_agent.publish_result(res, parser)  # publish result to MQ

    get_parser_by_name(parser)  # sanity check
    mq_type = get_url_scheme(mq_url)
    mq_agent_module = load_mq_agent(mq_type)
    mq_agent = mq_agent_module.MQAgent(mq_url)
    logger.info(f'starting to consume mq: {parser=}')
    mq_agent.consume_snapshots(callback, parser)  # start consuming the MQ
