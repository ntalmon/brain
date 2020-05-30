"""
The base DB agent provides an abstract class for DB agent implementations.
"""

import abc


class BaseDBAgent(abc.ABC):
    """
    The base DB agent abstract class should be inherited and implemented by DB agents.

    :param url: DB address.
    """

    def __init__(self, url: str):
        self.url = url

    @abc.abstractmethod
    def find_users(self) -> list:
        """
        Find all users in database.

        :return: list of user_id and username per user.
        """

        pass

    @abc.abstractmethod
    def find_user(self, user_id: int) -> dict:
        """
        Find user in database by user id.

        :param user_id: user id of the user.
        :return: user_id, username, birthday, and gender of the user.
        """

        pass

    @abc.abstractmethod
    def find_snapshots(self, user_id: int) -> list:
        """
        Find all snapshots of a user by user id.

        :param user_id: user id of the user.
        :return: list of uuid and datetime per snapshot.
        """

        pass

    @abc.abstractmethod
    def find_snapshot(self, user_id: int, snapshot_id: int) -> dict:
        """
        Find a snapshot by user id and snapshot id.

        :param user_id: user id of the user.
        :param snapshot_id: snapshot id of the snapshot.
        :return: uuid, datetime, and available results names of the snapshot.
        """

        pass

    @abc.abstractmethod
    def find_result(self, user_id: int, snapshot_id: int, result_name: str) -> dict:
        """
        Find result of a snapshot by user id, snapshot id, and result name.

        :param user_id: user id of the user.
        :param snapshot_id: snapshot id of the snapshot.
        :param result_name: name of the result.
        :return: the result as dictionary.
        """

        pass
