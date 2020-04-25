"""
TODO: design decision, consume single queue and infer topic from data, or consume multiple dedicated queues
"""
import json

from .db_agent import DBAgent
from .mq_agent import MQAgent
from brain.parsers import get_parsers

topics = get_parsers()


class Saver:
    def __init__(self, url):
        self.agent = DBAgent(url)

    def save(self, data):
        data = json.loads(data)  # TODO: parsers-saver protocol should be separated
        snapshot_id, timestamp, user_data, result = data['uuid'], data['datetime'], data['user'], data['result']
        user_id = user_data.pop('user_id')
        self.agent.save_result(user_id, user_data, snapshot_id, timestamp, result)


def run_saver(db_url, mq_url):
    saver = Saver(db_url)
    mq_agent = MQAgent(mq_url)
    mq_agent.consume_results(saver.save, topics)
