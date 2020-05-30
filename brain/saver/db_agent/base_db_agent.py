"""
The base DB agent module provides an abstract class for DB agent implementations.
"""

import abc


class BaseDBAgent(abc.ABC):
    """
    The base DB agent abstract class should be inherited and implemented by DB agents.

    :param url: DB address.
    """

    def __init__(self, url):
        self.url = url

    @abc.abstractmethod
    def save_result(self, topic: str, user_id: int, user_data: dict, snapshot_id: int, timestamp: int, result: dict):
        """
        Save single result to the database.

        :param topic: the result's topic.
        :param user_id: user id of the result.
        :param user_data: dictionary contains user details.
        :param snapshot_id: id of the snapshot.
        :param timestamp: timestamp of the snapshot.
        :param result: result to save.
        """

        pass
