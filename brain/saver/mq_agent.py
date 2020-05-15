from brain.utils.mq.rabbitmq import RabbitMQ


class MQAgent:
    def __init__(self, url):
        self.utils = RabbitMQ(url)

    def consume_results(self, callback, topics):
        def callback_wrapper(data, queue):
            topic = queue[len('saver_'):]
            return callback(topic, data)

        self.utils.consume(callback_wrapper, 'saver', [f'saver_{topic}' for topic in topics], exchange_type='direct')
