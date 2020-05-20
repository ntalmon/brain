from brain.utils.rabbitmq import RabbitMQ


class MQAgent:
    def __init__(self, url):
        self.utils = RabbitMQ(url)

    def consume_snapshots(self, callback, topic):
        self.utils.consume(callback, 'snapshot', [topic])

    def publish_result(self, result, topic):
        self.utils.publish(result, exchange='saver', queue=f'saver_{topic}')  # TODO: find right exchange and queue
