from furl import furl

from brain.db.mongodb import MongoDBAgent

drivers = {

    'mongodb': MongoDBAgent
}


def find_driver(url):
    scheme = furl(url).scheme
    if scheme not in drivers:
        return None  # TODO: handle this case
    return drivers[scheme]


class DBAgent:
    def __init__(self, url):
        agent_type = find_driver(url)
        self._agent = agent_type(url) if agent_type else None

    def save(self, topic, data):
        return self._agent.save(topic, data)
