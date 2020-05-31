"""
The saver module contains the main logic of the saver, which is, to save results and run the saver as a service.
"""

import json

from brain.parsers import get_parsers
from brain.utils.common import get_logger, get_url_scheme
from .db_agent import load_db_agent
from .mq_agent import load_mq_agent

logger = get_logger(__name__)
topics = get_parsers()


class Saver:
    """
    The Saver class provides the saving functionality.

    :param url: the database address.
    """

    def __init__(self, url: str):
        logger.info(f'initializing saver: {url=}')
        db_type = get_url_scheme(url)
        db_agent_module = load_db_agent(db_type)
        self.agent = db_agent_module.DBAgent(url)

    def save(self, topic: str, data: str):
        """
        Save results to a dedicated topic in the database.

        :param topic: the topic of the provided data.
        :param data: data to save, in JSON format.
        """

        logger.debug(f'saving data for {topic=}')
        data = json.loads(data)  # load data from JSON format
        snapshot_id, timestamp, user_data, result = data['uuid'], data['datetime'], data['user'], data['result']
        user_id = user_data.pop('user_id')
        self.agent.save_result(topic, user_id, user_data, snapshot_id, timestamp, result)


def run_saver(db_url, mq_url):
    """
    Run the saver as a service.

    :param db_url: address of the database.
    :param mq_url: address of the MQ to consume results from.
    """

    logger.info(f'running saver: {db_url=}, {mq_url=}')
    saver = Saver(db_url)
    mq_type = get_url_scheme(mq_url)
    mq_agent_module = load_mq_agent(mq_type)
    mq_agent = mq_agent_module.MQAgent(mq_url)
    logger.info(f'starting to consume data from mq')
    mq_agent.consume_results(saver.save, topics)
