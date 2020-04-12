"""
TODO: design decision, consume single queue and infer topic from data, or consume multiple dedicated queues
"""
import json

from brain.db import DBAgent
from brain.mq import MQAgent
from brain.parsers import get_parsers

topics = get_parsers()


class Saver:
    def __init__(self, url):
        self.agent = DBAgent(url)

    def save(self, topic, data):
        data = json.loads(data)  # TODO: parsers-saver protocol should be separated
        # TODO: continue implementation
        uuid, timestamp, user, res = data['uuid'], data['datetime'], data['user'], data['res']
        self.agent.save(topic, data)


def run_saver(db_url, mq_url):
    saver = Saver(db_url)
    mq_agent = MQAgent(mq_url)
    mq_agent.multi_consume(saver.save, exchange='saver', queues=topics)  # TODO: should give saver.save directly?
