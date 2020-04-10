import pymongo


class MongoDBAgent:
    def __init__(self, url):
        self.url = url
        # TODO: handle case where connection fails or db does not exist
        self.client = pymongo.MongoClient(self.url)
        self.db = self.client['brain']

    def save(self, topic, data):
        collection = self.db[topic]  # TODO: handle case where topic does not exist
        collection.insert_one()  # TODO: find what to insert


