from brain.utils.mq.rabbitmq import RabbitMQ


class MQAgent:
    def __init__(self, url):
        self.utils = RabbitMQ(url)

    def consume_results(self, callback, topics):
        self.utils.multi_consume(callback, exchange='saver', queues=topics)
