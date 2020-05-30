"""
The MQ agent provides an interface for the server to communicate with the MQ.

While the interface with the MQ agent remains the same, its implementation might change depending on the MQ
we're using. Therefore, it uses dynamic importing in order to import from the right MQ agent module.
"""

import types

from brain.utils.consts import MQType


def load_mq_agent(mq_type: MQType) -> types.ModuleType('mq_agent'):
    """
    Dynamically import the MQ agent module depending on the MQ, and return the imported module.

    :param mq_type: which MQ we're using.
    :return: the imported module.
    :raises: NotImplementedError is MQ is unsupported.
    """

    if mq_type == MQType.RABBITMQ.value:
        from . import rabbitmq_agent
        return rabbitmq_agent
    raise NotImplementedError(f'Unsupported MQ type: {mq_type}, could not import MQ agent')
