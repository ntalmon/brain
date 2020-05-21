from brain.utils.mongodb import MongoDB


class DBAgent(MongoDB):
    def find_users(self):
        users_list = self.find({}, {'_id': 0, 'user_id': 1, 'username': 1})
        users_list = list(users_list)
        return users_list

    def find_user(self, user_id):
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        user = self.find_one({'_id': user_id}, {'_id': 0, 'snapshots': 0})
        return user

    def find_snapshots(self, user_id):
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        snapshots = self.find_one({'_id': user_id},
                                  {'_id': 0, 'snapshots.uuid': 1, 'snapshots.datetime': 1})
        if snapshots is None:
            return snapshots
        return snapshots['snapshots']

    def find_snapshot(self, user_id, snapshot_id, include_path=False):
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        snapshot_id = str(snapshot_id)  # TODO: temporary workaround!!! should solve it
        if include_path:
            snapshot = self.find_one({'_id': user_id},
                                     {'snapshots': {'$elemMatch': {'_id': snapshot_id}}, '_id': 0,
                                      'snapshots.uuid': 1, 'snapshots.datetime': 1, 'snapshots.results': 1,
                                      'snapshots.path': 1})
        else:
            snapshot = self.find_one({'_id': user_id},
                                     {'snapshots': {'$elemMatch': {'_id': snapshot_id}}, '_id': 0,
                                      'snapshots.uuid': 1, 'snapshots.datetime': 1, 'snapshots.results': 1})
        if not snapshot:
            return snapshot
        snapshots = snapshot['snapshots']
        if not snapshots:
            return None
        snapshot = snapshots[0]
        snapshot['results'] = list(snapshot['results'].keys())
        return snapshot

    def find_snapshot_result(self, user_id, snapshot_id, result_name):
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        snapshot_id = str(snapshot_id)  # TODO: temporary workaround!!! should solve it
        entry = self.find_one({'_id': user_id}, {'snapshots': {'$elemMatch': {'_id': snapshot_id}}, '_id': 0,
                                                 f'snapshots.results.{result_name}': 1})
        if not entry:
            return None
        results = entry['snapshots'][0]['results']
        if result_name not in results:
            return None
        result = results[result_name]
        return result
