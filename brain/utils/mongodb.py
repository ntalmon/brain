import pymongo
import pymongo.database

from brain.utils.consts import *


class MongoDB:
    def __init__(self, url=''):
        self.url = url
        self.client = None  # type: pymongo.MongoClient
        self.db = None  # type: pymongo.database.Database
        self.collection = None  # type: pymongo.collection.Collection
        self._is_connected = False
        if self.url:
            self.connect(self.url)

    def connect(self, url):
        if self._is_connected:
            raise Exception('Cannot connect to database, already connected')

        self.url = url
        self.client = pymongo.MongoClient(self.url)
        self.db = self.client[DB_NAME]
        self.collection = self.db[COLLECTION_NAME]
        self._is_connected = True

    def _check_connection(self):
        if not self._is_connected:
            raise Exception('Database is not connected, cannot access')

    def find(self, *args, **kwargs):
        self._check_connection()
        return self.collection.find(*args, **kwargs)

    def find_one(self, *args, **kwargs):
        self._check_connection()
        return self.collection.find_one(*args, **kwargs)

    def insert_one(self, *args, **kwargs):
        self._check_connection()
        return self.collection.insert_one(*args, **kwargs)

    def insert_many(self, *args, **kwargs):
        self._check_connection()
        return self.collection.insert_many(*args, **kwargs)

    def update_one(self, *args, **kwargs):
        self._check_connection()
        return self.collection.update_one(*args, **kwargs)

    def update_many(self, *args, **kwargs):
        self._check_connection()
        return self.collection.update_many(*args, **kwargs)
