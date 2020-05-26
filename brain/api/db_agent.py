"""
The database agent provides an interface for the API
to communicate with the database.
The module provides the following interface:

class DBAgent:
    def __init__(self, url)
    def find_users(self)
    def find_user(self, user_id)
    def find_snapshots(self, user_id)
    def find_snapshot(self, user_id, snapshot_id)
    def find_result(self, user_id, snapshot_id, result_name)
"""
from brain.utils.common import get_logger
from brain.utils.mongodb import MongoDB

logger = get_logger(__name__)


class DBAgent(MongoDB):
    """
    Provides the API->database communication.
    """
    def __init__(self, url):
        MongoDB.__init__(self, url)

    def find_users(self):
        """
        Find all users in database.
        :return list of user_id and username per user.
        """
        # _id is used for "db uniqueness" only, fetch user_id and username
        users_list = self.find({}, {'_id': 0, 'user_id': 1, 'username': 1})
        users_list = list(users_list)
        return users_list

    def find_user(self, user_id):
        """
        Find user in database by user id.
        :return: user_id, username, birthday, and gender of the user.
        """
        logger.debug(f'fetching all users from database')
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        # exclude _id snapshots list
        user = self.find_one({'_id': user_id}, {'_id': 0, 'snapshots': 0})
        return user

    def find_snapshots(self, user_id):
        """
        Find all snapshots of a user by user id.
        :return: list of uuid and datetime per snapshot.
        """
        logger.debug(f'fetching snapshot from database, {user_id=}')
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        # take only uuid and datetime from snapshots
        snapshots = self.find_one({'_id': user_id},
                                  {'_id': 0, 'snapshots.uuid': 1, 'snapshots.datetime': 1})
        if snapshots is None:
            logger.info(f'could not find entry with {user_id=}')
            return snapshots
        return snapshots['snapshots']

    def find_snapshot(self, user_id, snapshot_id, include_path=False):
        """
        Find a snapshot by user id and snapshot id.
        :return: uuid, datetime, and available results names of the snapshot.
        """
        logger.debug(f'fetching snapshot from database, {user_id=}, {snapshot_id=}')
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        snapshot_id = str(snapshot_id)  # TODO: temporary workaround!!! should solve it
        # take uuid, datetime, results, and optionally path from snapshot
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
            logger.info(f'could not find entry with {user_id=}, {snapshot_id=}')
            return None
        snapshots = snapshot['snapshots']
        snapshot = snapshots[0]
        # do not return the full results, only names
        snapshot['results'] = list(snapshot['results'].keys())
        return snapshot

    def find_snapshot_result(self, user_id, snapshot_id, result_name):
        """
        Find result of a snapshot by user id, snapshot id, and result name.
        :return: the result.
        """
        logger.debug(f'fetching snapshot result from database, {user_id=}, {snapshot_id=}, {result_name=}')
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        snapshot_id = str(snapshot_id)  # TODO: temporary workaround!!! should solve it
        # take result from snapshot results
        entry = self.find_one({'_id': user_id}, {'snapshots': {'$elemMatch': {'_id': snapshot_id}}, '_id': 0,
                                                 f'snapshots.results.{result_name}': 1})
        if not entry:
            logger.info(f'could not find entry with {user_id=}, {snapshot_id=}')
            return None
        results = entry['snapshots'][0]['results']
        if result_name not in results:
            logger.info(f'could not find entry with {user_id=}, {snapshot_id=}, {result_name=}')
            return None
        result = results[result_name]
        return result
