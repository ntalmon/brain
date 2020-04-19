from brain.utils.mq.rabbitmq import RabbitMQ


class RabbitMQAgent:
    def __init__(self, url):
        self.utils = RabbitMQ(url)

    def publish_snapshot(self, snapshot):
        self.utils.publish(snapshot, exchange='snapshot')
