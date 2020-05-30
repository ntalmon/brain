"""
The DB agent provides an interface for the API to communicate with the database.

While the interface with the DB agent remains the same, its implementation might change depending on the database
we're using. Therefore, it uses dynamic importing in order to import from the right DB agent module.
"""

import types

from brain.utils.consts import DBType


def load_db_agent(database: DBType) -> types.ModuleType('db_agent'):
    """
    Dynamically import the DB agent module depending on the database, and return the imported module.

    :param database: which DB we're using.
    :return: the imported module.
    :raises: NotImplementedError is database is unsupported.
    """

    if database == DBType.MONGODB.value:
        from . import mongodb_agent
        return mongodb_agent
    raise NotImplementedError(f'Invalid database: {database}, could not import DB agent')
