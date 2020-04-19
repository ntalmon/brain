from brain.utils.mq.rabbitmq import RabbitMQ


class RabbitMQAgent:
    def __init__(self, url):
        self.utils = RabbitMQ(url)

    def consume_snapshots(self, callback, topic):
        self.utils.consume(callback, exchange='snapshot', queue=topic)

    def publish_result(self, result, topic):
        self.utils.publish(result, queue=f'saver_{topic}')  # TODO: find right exchange and queue
