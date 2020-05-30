"""
The server agent provides an interface for the client to communicate with the server.

While the interface with the server agent remains the same, its implementation might change
depending on client-server protocol. Therefore, it uses dynamic importing in order to import
from the right server agent module.
"""
import types

from brain.utils.consts import ProtocolType


def load_server_agent(protocol: ProtocolType) -> types.ModuleType('server_agent'):
    """
    Dynamically import the server agent module depending on the client-server protocol, and return the imported module.

    :param protocol: client-server protocol.
    :return: the imported module.
    :raises: NotImplementedError is protocol is unsupported.
    """

    if protocol == ProtocolType.HTTP.value:
        from . import http_server_agent
        return http_server_agent
    raise NotImplementedError(f'Unsupported protocol: {protocol}, could not import server agent')
