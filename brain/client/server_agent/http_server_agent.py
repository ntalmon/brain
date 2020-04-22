import requests
from furl import furl


class HTTPServerAgent:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.url = furl(scheme='http', host=host, port=port)

    def send_snapshot(self, snapshot):
        request = self.url / 'snapshot'
        snapshot_msg = snapshot.SerializeToString()
        response = requests.post(request, snapshot_msg)
        if response.status_code != 200:
            raise Exception()  # TODO: handle this case
