"""
The DB agent module provides an interface for the saver to save results to database.
"""
from typing import Any

from brain.utils.common import get_logger
from brain.utils.mongodb import MongoDB

logger = get_logger(__name__)


class DBAgent(MongoDB):
    """
    The DB agent class connects to the database and allows saving results to it.
    """

    def _create_user_if_not_exist(self, user_id, user_entry):
        res = self.update_one(
            {'_id': user_id},
            {'$setOnInsert': user_entry},
            upsert=True
        )
        return bool(res.upserted_id)

    def _create_snapshot_if_not_exist(self, user_id, snapshot_id, snapshot_entry):
        res = self.update_one(
            {'_id': user_id, 'snapshots._id': {'$nin': [snapshot_id]}},
            {'$push': {'snapshots': snapshot_entry}}
        )
        return bool(res.matched_count)

    def _add_result_to_snapshot(self, topic, user_id, snapshot_id, result_entry):
        # TODO: handle update_one return value
        self.update_one(
            {'_id': user_id, 'snapshots._id': snapshot_id},
            {'$set': {f'snapshots.$.results.{topic}': result_entry}}
        )

    def save_result(self, topic: str, user_id: int, user_data: dict, snapshot_id: int, timestamp: int, result: Any):
        """
        Save single result to the database.

        :param topic: the result's topic.
        :param user_id: user id of the result.
        :param user_data: dictionary contains user details.
        :param snapshot_id: id of the snapshot.
        :param timestamp: timestamp of the snapshot.
        :param result: result to save.
        """
        
        logger.debug(f'saving result to db: {topic=}, {user_id=}, {user_data=}, {snapshot_id=}, {timestamp=}')
        snapshot_entry = {'_id': snapshot_id, 'uuid': snapshot_id, 'datetime': timestamp, 'results': {topic: result}}
        user_entry = {'_id': user_id, 'user_id': user_id, **user_data, 'snapshots': [snapshot_entry]}
        if self._create_user_if_not_exist(user_id, user_entry):
            return
        if self._create_snapshot_if_not_exist(user_id, snapshot_id, snapshot_entry):
            return
        self._add_result_to_snapshot(topic, user_id, snapshot_id, result)
