from furl import furl

from brain.saver.mq_agent.rabbitmq_agent import RabbitMQAgent

agents = {
    'rabbitmq': RabbitMQAgent
}


def get_mq_agent(url):
    scheme = furl(url).scheme
    return agents[scheme]  # TODO: handle this case
