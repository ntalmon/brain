import json

from brain.parsers import get_parsers
from .db_agent import DBAgent
from .mq_agent import MQAgent

topics = get_parsers()


class Saver:
    def __init__(self, url):
        self.agent = DBAgent(url)

    def save(self, topic, data):
        data = json.loads(data)  # TODO: parsers-saver protocol should be separated
        snapshot_id, timestamp, user_data, result = data['uuid'], data['datetime'], data['user'], data['result']
        user_id = user_data.pop('user_id')
        self.agent.save_result(topic, user_id, user_data, snapshot_id, timestamp, result)


def run_saver(db_url, mq_url):
    saver = Saver(db_url)
    mq_agent = MQAgent(mq_url)
    mq_agent.consume_results(saver.save, topics)
