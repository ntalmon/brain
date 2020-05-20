from brain.utils.rabbitmq import RabbitMQ


class MQAgent:
    def __init__(self, url):
        self.utils = RabbitMQ(url)

    def publish_snapshot(self, snapshot):
        self.utils.publish(snapshot, exchange='snapshot')
