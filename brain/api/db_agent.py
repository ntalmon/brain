"""
The database agent provides an interface for the API to communicate with the database.
"""

from brain.utils.common import get_logger
from brain.utils.mongodb import MongoDB

logger = get_logger(__name__)


class DBAgent(MongoDB):
    """
    The DBAgent agent class provides multiple entry points to fetch data from the database.
    """

    def find_users(self) -> list:
        """
        Find all users in database.

        :return: list of user_id and username per user.
        """

        # _id is used for "db uniqueness" only, fetch user_id and username
        users_list = self.find({}, {'_id': 0, 'user_id': 1, 'username': 1})
        users_list = list(users_list)
        return users_list

    def find_user(self, user_id: int) -> dict:
        """
        Find user in database by user id.

        :return: user_id, username, birthday, and gender of the user.
        """

        logger.debug(f'fetching all users from database')
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        # exclude _id snapshots list
        user = self.find_one({'_id': user_id}, {'_id': 0, 'snapshots': 0})
        return user

    def find_snapshots(self, user_id: int) -> list:
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

    def find_snapshot(self, user_id: int, snapshot_id: int, include_path: bool = False) -> dict:
        """
        Find a snapshot by user id and snapshot id.

        :return: uuid, datetime, and available results names of the snapshot.
        """

        logger.debug(f'fetching snapshot from database, {user_id=}, {snapshot_id=}')
        user_id = str(user_id)  # TODO: temporary workaround!!! should solve it
        snapshot_id = str(snapshot_id)  # TODO: temporary workaround!!! should solve it
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

    def find_snapshot_result(self, user_id: int, snapshot_id: int, result_name: str) -> dict:
        """
        Find result of a snapshot by user id, snapshot id, and result name.

        :return: the result as dictionary.
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
