"""
The DB agent provides an interface for the saver to communicate with the database.

While the interface with the DB agent remains the same, its implementation might change depending on the database
we're using. Therefore, it uses dynamic importing in order to import from the right DB agent module.
"""

import types

from brain.utils.consts import DBType


def load_db_agent(db_type: DBType) -> types.ModuleType('db_agent'):
    """
    Dynamically import the DB agent module depending on the database, and return the imported module.

    :param db_type: which DB we're using.
    :return: the imported module.
    :raises: NotImplementedError is database is unsupported.
    """

    if db_type == DBType.MONGODB.value:
        from . import mongodb_agent
        return mongodb_agent
    raise NotImplementedError(f'Invalid database: {db_type}, could not import DB agent')
