"""
TODO: design decision, consume single queue and infer topic from data, or consume multiple dedicated queues
"""
from brain.db import DBAgent
from brain.mq import MQAgent

topics = ['pose']  # TODO: handle way of finding all topics


class Saver:
    def __init__(self, url):
        self.agent = DBAgent(url)

    def save(self, topic, data):
        pass


def run_saver(db_url, mq_url):
    saver = Saver(db_url)
    mq_agent = MQAgent(mq_url)
    mq_agent.multi_consume(saver.save, exchange='saver', queues=topics)  # TODO: should give saver.save directly?


if __name__ == '__main__':
    from brain.cli.saver import run_cli

    run_cli()
