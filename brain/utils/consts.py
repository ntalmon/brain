"""
The consts module provides some constants used by the brain package and by some tests.
"""

from enum import Enum

import yaml
from furl import furl

from brain import config_path

with open(str(config_path), 'r') as _conf_reader:
    config = yaml.load(_conf_reader, Loader=yaml.Loader)

API_HOST, DB_HOST, GUI_HOST, MQ_HOST, SERVER_HOST = [config['hosts'][_i] for _i in ['api', 'db', 'gui', 'mq', 'server']]

API_PORT, DB_PORT, GUI_PORT, MQ_PORT, SERVER_PORT = [config['ports'][_i] for _i in ['api', 'db', 'gui', 'mq', 'server']]

API_URL = f'http://{API_HOST}:{API_PORT}'
DB_URL = f'mongodb://{DB_HOST}:{DB_PORT}'
GUI_URL = f'http://{GUI_HOST}:{GUI_PORT}'
MQ_URL = f'rabbitmq://{MQ_HOST}:{MQ_PORT}'

API_FURL = furl(API_URL)
DB_FURL = furl(DB_URL)
GUI_FURL = furl(GUI_URL)
MQ_FURL = furl(MQ_URL)

DB_NAME = 'brain'
COLLECTION_NAME = 'users_and_snapshots'

PARSERS = ['pose', 'color_image', 'depth_image', 'feelings']


class FileFormat(Enum):
    NATIVE = config['formats']['native']
    GZIP = config['formats']['gzip']


class MessageFormat(Enum):
    MIND = config['formats']['mind']


class ProtocolType(Enum):
    HTTP = config['protocols']['http']


class DBType(Enum):
    MONGODB = config['db_types']['mongodb']


class MQType(Enum):
    RABBITMQ = config['mq_types']['rabbitmq']
