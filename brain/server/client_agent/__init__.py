"""
The client agent provides an interface for the server to accept connection and receive snapshots from clients.
It runs as a server that receives messages, parses them and then passes them to the server (brain.server.server)
by calling registered handlers.

While the interface with the client agent remains the same, its implementation might change
depending on client-server protocol. Therefore, it uses dynamic importing in order to import
from the right client agent module.
"""

import types

from brain.utils.consts import ProtocolType


def load_client_agent(protocol: ProtocolType) -> types.ModuleType('server_agent'):
    """
    Dynamically import the client agent module depending on the client-server protocol, and return the imported module.

    :param protocol: client-server protocol.
    :return: the imported module.
    :raises: NotImplementedError is protocol is unsupported.
    """

    if protocol == ProtocolType.HTTP.value:
        from . import http_client_agent
        return http_client_agent
    raise NotImplementedError(f'Unsupported protocol: {protocol}, could not import client agent')
