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
            self.channel.exchange_declare(exchange, exchange_type='fanout')
            queue = self.channel.queue_declare(queue, exclusive=True).name
            self.channel.queue_bind(queue, exchange)
        else:
            self.channel.queue_declare(queue)

        def cb_wrapper(channel, method, properties, body):
            callback(body)

        self.channel.basic_consume(queue, cb_wrapper, auto_ack=True)
        self.channel.start_consuming()

    def publish(self, data, exchange='', queue=''):
        if not exchange and not queue:
            return  # TODO: handle this case

        self.channel.basic_publish(exchange, queue, data)
