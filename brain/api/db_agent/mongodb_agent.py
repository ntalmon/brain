"""
The mongodb agent provides an interface for the API to communicate with the database, with mongodb implementation.
"""

from brain.api.db_agent.base_db_agent import BaseDBAgent
from brain.utils.common import get_logger
from brain.utils.mongodb import MongoDB

logger = get_logger(__name__)


class DBAgent(MongoDB, BaseDBAgent):
    """
    Mongodb-based implementation of DB agent.

    This implementation has single collection that contains an entry per user.
    Each user entry contains its details, and list of snapshots.
    Each snapshot entry in the list contains its details and available results.
    """

    def find_users(self) -> list:
        # _id is used for "db uniqueness" only, fetch user_id and username
        users_list = self.find({}, {'_id': 0, 'user_id': 1, 'username': 1})
        users_list = list(users_list)
        return users_list

    def find_user(self, user_id: int) -> dict:
        logger.debug(f'fetching all users from database')
        user_id = str(user_id)
        # exclude _id snapshots list
        user = self.find_one({'_id': user_id}, {'_id': 0, 'snapshots': 0})
        return user

    def find_snapshots(self, user_id: int) -> list:
        logger.debug(f'fetching snapshot from database, {user_id=}')
        user_id = str(user_id)
        # take only uuid and datetime from snapshots
        snapshots = self.find_one({'_id': user_id},
                                  {'_id': 0, 'snapshots.uuid': 1, 'snapshots.datetime': 1})
        if snapshots is None:
            logger.info(f'could not find entry with {user_id=}')
            return snapshots
        return snapshots['snapshots']

    def find_snapshot(self, user_id: int, snapshot_id: int, include_path: bool = False) -> dict:
        logger.debug(f'fetching snapshot from database, {user_id=}, {snapshot_id=}')
        user_id = str(user_id)
        snapshot_id = str(snapshot_id)
        projection = {'snapshots': {'$elemMatch': {'_id': snapshot_id}}, '_id': 0,
                      'snapshots.uuid': 1, 'snapshots.datetime': 1, 'snapshots.results': 1}
        if include_path:
            projection['snapshots.path'] = 1
        snapshot = self.find_one({'_id': user_id}, projection)
        if not snapshot:
            logger.info(f'could not find entry with {user_id=}, {snapshot_id=}')
            return None
        snapshots = snapshot['snapshots']
        snapshot = snapshots[0]
        # do not return the full results, only names
        snapshot['results'] = list(snapshot['results'].keys())
        return snapshot

    def find_result(self, user_id: int, snapshot_id: int, result_name: str) -> dict:
        logger.debug(f'fetching snapshot result from database, {user_id=}, {snapshot_id=}, {result_name=}')
        user_id = str(user_id)
        snapshot_id = str(snapshot_id)
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
