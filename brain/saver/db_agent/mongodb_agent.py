"""
The MongoDB agent module provides a DB agent with MongoDB implementation.
"""

from typing import Any

from brain.saver.db_agent.base_db_agent import BaseDBAgent
from brain.utils.common import get_logger
from brain.utils.mongodb import MongoDB

logger = get_logger(__name__)


class DBAgent(MongoDB, BaseDBAgent):
    """
    MongoDB-based implementation of DB agent.

    This implementation has single collection that contains an entry per user.
    Each user entry contains its details, and list of snapshots.
    Each snapshot entry in the list contains its details and available results.
    All database update operations are atomic, so there shouldn't be any race conditions.
    """

    def _create_user_if_not_exist(self, user_id, user_entry):
        # add user entry to the database if user id does not exist
        res = self.update_one(
            {'_id': user_id},
            {'$setOnInsert': user_entry},
            upsert=True
        )
        return bool(res.upserted_id)

    def _create_snapshot_if_not_exist(self, user_id, snapshot_id, snapshot_entry):
        # add snapshot entry to snapshots list of a user if snapshot id does not exist
        res = self.update_one(
            {'_id': user_id, 'snapshots._id': {'$nin': [snapshot_id]}},
            {'$push': {'snapshots': snapshot_entry}}
        )
        return bool(res.matched_count)

    def _add_result_to_snapshot(self, topic, user_id, snapshot_id, result_entry):
        # add result to the snapshot results
        self.update_one(
            {'_id': user_id, 'snapshots._id': snapshot_id},
            {'$set': {f'snapshots.$.results.{topic}': result_entry}}
        )

    def save_result(self, topic: str, user_id: int, user_data: dict, snapshot_id: int, timestamp: int, result: Any):
        user_id = str(user_id)
        logger.debug(f'saving result to db: {topic=}, {user_id=}, {user_data=}, {snapshot_id=}, {timestamp=}')
        # entry contains snapshot details and results
        snapshot_entry = {'_id': snapshot_id, 'uuid': snapshot_id, 'datetime': timestamp, 'results': {topic: result}}
        # entry contains user details and the snapshot details of the given snapshot (snapshot_entry)
        user_entry = {'_id': user_id, 'user_id': user_id, **user_data, 'snapshots': [snapshot_entry]}
        # try to insert the user entry first
        if self._create_user_if_not_exist(user_id, user_entry):
            return  # user entry was added and all the required data is in database now; return
        # user already exists, try to update only the snapshot entry
        if self._create_snapshot_if_not_exist(user_id, snapshot_id, snapshot_entry):
            return  # snapshot entry was added and all the required data is in database now; return
        # snapshot already exists, just add the result
        self._add_result_to_snapshot(topic, user_id, snapshot_id, result)
