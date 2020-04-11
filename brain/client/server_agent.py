"""
TODO: use design pattern for client agents
"""
import requests
from furl import furl

from brain.autogen import protocol_pb2


class HTTPServerAgent:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = furl(scheme='http', host=host, port=port)

    def get_config(self):
        request = self.url / 'config'
        response = requests.get(request)
        if response.status_code != 200:
            return None  # TODO: handle this case
        config = protocol_pb2.Config()
        config.ParseFromString(response.text)
        return config

    def send_snapshot(self, snapshot):
        request = self.url / 'snapshot'
        snapshot_msg = snapshot.SerializeToString()
        response = requests.post(request, snapshot_msg)
        if response.status_code != 200:
            return None  # TODO: handle this case
