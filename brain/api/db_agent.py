import pymongo


class MongoDBAgent:
    def __init__(self, url):
        self.client = pymongo.MongoClient(url)
        self.db = self.client['brain']
        self.users = self.db['users']

    def find_users(self):
        users_list = self.users.find({}, {'_id': 1})
        return users_list  # TODO: handle case of empty result

    def find_user(self, user_id):
        self.users.distinct()
        user = self.users.find_one({'_id': user_id})
        return user  # TODO: handle case of empty result

    def find_snapshots(self, user_id):
        snapshots = self.users.find({'_id': user_id}, {'_id': 0, 'snapshots': 1})
        return snapshots  # TODO: handle case of empty result

    def _find_snapshot(self, user_id, snapshot_id):
        snapshot = self.users.find({'_id': user_id}, {'snapshots': {'$elemMatch': {'_id': snapshot_id}}})
        return snapshot  # TODO: handle case of empty result

    def find_snapshot(self, user_id, snapshot_id):
        snapshot = self._find_snapshot(user_id, snapshot_id)
        return snapshot['results'].keys()

    def find_snapshot_result(self, user_id, snapshot_id, result_name):
        snapshot = self._find_snapshot(user_id, snapshot_id)
        return snapshot['results'][result_name]  # TODO: handle this case
