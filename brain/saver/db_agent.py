import pymongo


class DBAgent:
    def __init__(self, url):
        self.url = url
        # TODO: handle case where connection fails or db does not exist
        self.client = pymongo.MongoClient(self.url)
        self.db = self.client['brain']
        self.users = self.db['users']

    def _create_user_if_not_exist(self, user_id, user_entry):
        res = self.users.update_one(
            {'_id': user_id},
            {'$setOnInsert': user_entry},
            upsert=True
        )
        return bool(res.upserted_id)

    def _create_snapshot_if_not_exist(self, user_id, snapshot_id, snapshot_entry):
        res = self.users.update_one(
            {'_id': user_id, 'snapshots._id': {'$nin': [snapshot_id]}},
            {'$push': {'snapshots': snapshot_entry}}
        )
        return bool(res.matched_count)

    def _add_result_to_snapshot(self, topic, user_id, snapshot_id, result_entry):
        # TODO: handle update_one return value
        self.users.update_one(
            {'_id': user_id, 'snapshots._id': snapshot_id},
            {'$set': {f'snapshots.$.results.{topic}': result_entry}}
        )

    def save_result(self, topic, user_id, user_data, snapshot_id, timestamp, result):
        # TODO: handle return value
        snapshot_entry = {'_id': snapshot_id, 'timestamp': timestamp, 'results': {topic: result}}
        user_entry = {'_id': user_id, **user_data, 'snapshots': [snapshot_entry]}
        if self._create_user_if_not_exist(user_id, user_entry):
            return
        if self._create_snapshot_if_not_exist(user_id, snapshot_id, snapshot_entry):
            return
        self._add_result_to_snapshot(topic, user_id, snapshot_id, result)
