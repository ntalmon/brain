"""
The server package receives snapshots from the clients and sends them to the parsers via a MQ.
"""

from .server import run_server, construct_publish
