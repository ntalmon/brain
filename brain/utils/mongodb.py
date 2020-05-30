"""
The MongoDB module provides a common interface for a MongoDB connection and operations.
"""

import pymongo
import pymongo.database

from brain.utils.common import get_logger
from brain.utils.consts import *

logger = get_logger(__name__)


class MongoDB:
    """
    The Mongodb class first connect to the data, and provides multiple database operations.

    :param url: database address.
    """

    def __init__(self, url: str):
        logger.info(f'connecting MongoDB: {url=}')
        self.url = url
        self.client = pymongo.MongoClient(self.url)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]

    def find(self, *args, **kwargs):
        """
        Find in database. Args, kwargs and return value are like pymongo.database.Collection.find
        """

        return self.collection.find(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        """
        Find a single entry in database. Args, kwargs and return value are like pymongo.database.Collection.find_one.
        """

        return self.collection.find_one(*args, **kwargs)

    def update_one(self, *args, **kwargs):
        """
        Updates a single entry in database. Args, kwargs and return value are like
        pymongo.database.Collection.update_one.
        """

        return self.collection.update_one(*args, **kwargs)
