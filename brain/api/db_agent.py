import json

import pymongo


class MongoDBAgent:
    def __init__(self, url):
        self.client = pymongo.MongoClient(url)
        self.db = self.client['brain']
        self.users = self.db['users']

    def find_users(self):
        users_list = self.users.find({}, {'_id': 0, 'user_id': 1, 'username': 1})
        users_list = list(users_list)  # TODO: handle case of empty result
        return users_list

    def find_user(self, user_id):
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        user = self.users.find_one({'_id': user_id}, {'_id': 0, 'snapshots': 0})
        return user  # TODO: handle case of empty result

    def find_snapshots(self, user_id):
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        snapshots = self.users.find_one({'_id': user_id},
                                        {'_id': 0, 'snapshots.uuid': 1, 'snapshots.datetime': 1})
        return snapshots['snapshots']  # TODO: handle case of empty result

    def find_snapshot(self, user_id, snapshot_id):
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        snapshot_id = str(snapshot_id)  # TODO: temporary workaround!!! should solve it
        snapshot = self.users.find_one({'_id': user_id},
                                       {'snapshots': {'$elemMatch': {'_id': snapshot_id}}, '_id': 0,
                                        'snapshots.uuid': 1, 'snapshots.datetime': 1, 'snapshots.results': 1})
        snapshot = snapshot['snapshots'][0]  # TODO: handle case of empty result
        snapshot['results'] = list(snapshot['results'].keys())
        return snapshot

    def find_snapshot_result(self, user_id, snapshot_id, result_name):
        snapshot = self._find_snapshot(user_id, snapshot_id)
        return snapshot['results'][result_name]  # TODO: handle this case
