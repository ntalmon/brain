import pymongo


class DBAgent:
    def __init__(self, url):
        self.url = url
        # TODO: handle case where connection fails or db does not exist
        self.client = pymongo.MongoClient(self.url)
        self.db = self.client['brain']

    def save_metadata(self, user_id, user_data, timestamp, snapshot_id):
        users = self.db['users']
        # users.update_one(
        #     {'_id': user_id},
        #     {
        #         '$setOnInsert': {
        #             **user_data,
        #             'snapshots': []
        #         }
        #     },
        #     upsert=True
        # )
        # users.update_one(
        #     {'_id': user_id},
        #     {
        #
        #     }
        # )
        if not users.find_one({'_id': user_id}):
            _dict = {'_id': user_id, 'snapshots': [{'_id': snapshot_id, 'timestamp': timestamp}]}
            _dict.update(user_data)
            users.insert_one(_dict)
        else:
            users.update_one({'_id': user_id}, {
                '$push': {'snapshots': {
                    '_id': snapshot_id,
                    'datetime': timestamp
                }}
            })

    def save_data(self, topic, snapshot_id):
        pass
