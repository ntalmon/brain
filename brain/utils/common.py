"""
Provides some common utilities.
"""

import functools
import gzip
import logging
import pathlib
import sys
from typing import Union

from furl import furl
from google.protobuf import json_format
from google.protobuf.message import Message

from brain import log_path
from brain.utils.consts import FileFormat, config

fmt = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(level=logging.INFO, filename=str(log_path), format=fmt, datefmt=datefmt)


def get_logger(name: str) -> logging.Logger:
    """
    Get configured logger to be used by a module.

    :param name: module name (probably will by __name__ of the caller).
    :return: the logger object.
    """

    logger = logging.getLogger(name)
    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)
    return logger


def normalize_path(path: Union[str, pathlib.Path]) -> pathlib.Path:
    """
    Given a path as a string or pathlib.Path object, return it always as pathlib.Path.

    :param path: string or pathlib.Path.
    :return: pathlib.Path object.
    """

    return pathlib.Path(str(path))


def cli_suppress(f: callable, logger: logging.Logger = None) -> callable:
    """
    Common decorator used mainly by CLI function that runs some main function and handles errors.
    Must be the last decorator, or at least after all click decorators.

    :param f: the main function to be called (must be with no parameters).
    :param logger: optional logger to log errors to.
    :return: the wrapped function.
    """

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        try:
            f(*args, **kwargs)
        except Exception as error:
            logger and logger.error(f'error while running command: {error}')
            # check for config
            if config['debug']:
                raise
            logger and logger.info(f'exiting program: code=1')
            print(str(error))
            sys.exit(1)

    return wrapper


def get_file_stream_type(file_format):
    """
    Get file stream type according to a given file format.

    :param file_format: file format.
    :return: the file stream type, for example `open` or `gzip.open`
    :raises: NotImplementedError is file format is unsupported.
    """

    if file_format == FileFormat.NATIVE.value:
        return open
    if file_format == FileFormat.GZIP.value:
        return gzip.open
    raise NotImplementedError(f'Unsupported file format: {file_format}')


def get_url_scheme(url: str) -> str:
    """
    Get the scheme of URL. For example scheme of `http://localhost:8000` is `http`.

    :param url: get scheme of this URL.
    :return: the URL scheme.
    """

    url = furl(str(url))
    return url.scheme


def parse_protobuf(pb_object: Message, data: bytes) -> Message:
    """
    Given protobuf object, parse it from the given data.

    :param pb_object: the object to load data to.
    :param data: data to load to the object.
    :return: the protobuf object itself.
    """

    pb_object.ParseFromString(data)
    return pb_object


def serialize_protobuf(pb_object: Message) -> bytes:
    """
    Serialize protobuf object to bytes.

    :param pb_object: object to serialize.
    :return: the serialized bytes.
    """

    return pb_object.SerializeToString()


def protobuf2dict(pb_object: Message) -> dict:
    """
    Convert protobuf object to a dictionary.

    :param pb_object: object to convert.
    :return: the object dictionary.
    """

    return json_format.MessageToDict(pb_object, including_default_value_fields=True,
                                     preserving_proto_field_name=True)
