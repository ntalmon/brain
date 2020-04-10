import pika
from furl import furl


class RabbitMQAgent:
    """
    TODO: handle exchanges if needed
    """

    def __init__(self, url):
        self.url = url
        _url = furl(url)
        host, port = _url.host, _url.port
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()

    def consume(self, callback, exchange='', queue=''):
        if not exchange and not queue:
            return  # TODO: handle this case

        if exchange:
            self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
            # TODO: check the case of predefined queue name
            result = self.channel.queue_declare(queue=queue, exclusive=True)
            queue = result.method.queue
            self.channel.queue_bind(exchange=exchange, queue=queue)
        else:
            self.channel.queue_declare(queue=queue)

        def wrapper(channel, method, properties, body):
            return callback(body)

        self.channel.basic_consume(queue=queue, auto_ack=True, on_message_callback=wrapper)
        self.channel.start_consuming()

    def multi_consume(self, callback, exchange='', queues=None):
        if not queues:
            if not exchange:
                return  # TODO: handle this case
            queues = ['']

        if exchange:
            queue_names = []
            self.channel.exchange_declare(exchange=exchange, exchange_type='fanout')
            for queue in queues:
                # TODO: check the case of predefined queue name
                result = self.channel.queue_declare(queue=queue, exclusive=True)
                queue = result.method.queue
                queue_names.append(queue)
                self.channel.queue_bind(exchange=exchange, queue=queue)
        else:
            queue_names = queues
            for queue in queues:
                self.channel.queue_declare(queue=queue)

        for queue in queue_names:
            def wrapper(channel, method, properties, body):
                return callback(queue, body)

            self.channel.basic_consume(queue=queue, exchange=exchange, on_message_callback=wrapper)
            
        self.channel.start_consuming()

    def publish(self, data, exchange='', queue=''):
        if not exchange and not queue:
            return  # TODO: handle this case

        self.channel.basic_publish(exchange, queue, data)
