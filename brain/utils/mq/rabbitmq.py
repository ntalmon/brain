import pika
from furl import furl


class RabbitMQ:
    def __init__(self, url):
        self.url = url
        _url = furl(url)
        host, port = _url.host, _url.port
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()

    def consume(self, callback, exchange='', queue=''):
        if not exchange and not queue:
            raise Exception(f'Invalid parameters: expecting at least exchange or queue to be provided')

        if exchange:
            self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
            result = self.channel.queue_declare(queue=queue)
            queue = queue or result.method.queue  # in case that queue was not given
            self.channel.queue_bind(exchange=exchange, queue=queue)
        else:
            self.channel.queue_declare(queue=queue)

        def wrapper(channel, method, properties, body):
            res = callback(body)
            channel.basic_ack(delivery_tag=method.delivery_tag)
            return res

        self.channel.basic_consume(queue=queue, auto_ack=False, on_message_callback=wrapper)  # TODO: handle auto_ack
        self.channel.start_consuming()

    def multi_consume(self, callback, exchange='', queues=None):
        if not queues:
            if not exchange:
                raise Exception(f'Invalid parameters: expecting at least exchange or queue to be provided')
            queues = ['']

        if exchange:
            queue_names = []
            self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
            for queue in queues:
                # TODO: check the case of predefined queue name
                result = self.channel.queue_declare(queue=queue)
                queue = result.method.queue
                queue_names.append(queue)
                self.channel.queue_bind(exchange=exchange, queue=queue)
        else:
            queue_names = queues
            for queue in queues:
                self.channel.queue_declare(queue=queue)

        for queue in queue_names:
            def wrapper(channel, method, properties, body):
                res = callback(body)
                channel.basic_ack(delivery_tag=method.delivery_tag)
                return res

            self.channel.basic_consume(queue=queue, on_message_callback=wrapper)

        self.channel.start_consuming()

    def publish(self, data, exchange='', queue=''):
        if not exchange and not queue:
            return  # TODO: handle this case

        self.channel.basic_publish(exchange, queue, data)
