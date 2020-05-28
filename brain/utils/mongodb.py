import pymongo
import pymongo.database

from brain.utils.common import get_logger
from brain.utils.consts import *

logger = get_logger(__name__)


class MongoDB:
    def __init__(self, url: str):
        logger.info(f'connecting mongodb: {url=}')
        self.url = url
        self.client = pymongo.MongoClient(self.url)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def find(self, *args, **kwargs):
        return self.collection.find(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        return self.collection.find_one(*args, **kwargs)

    def update_one(self, *args, **kwargs):
        return self.collection.update_one(*args, **kwargs)
