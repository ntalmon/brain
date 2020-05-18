import pika
from furl import furl

stop_consuming_secret = b'Secret message, stop consuming'


class RabbitMQ:
    def __init__(self, url):
        self.url = url
        _url = furl(url)
        host, port = _url.host, _url.port
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
        self.channel = self.connection.channel()

    def close(self):
        self.channel.close()
        self.connection.close()

    def consume(self, callback, exchange, queues, exchange_type='fanout'):
        if exchange:
            self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        for queue in queues:
            self.channel.queue_declare(queue=queue)
            if exchange:
                self.channel.queue_bind(exchange=exchange, queue=queue)

        def wrapper(channel, method, properties, body):
            if body == stop_consuming_secret:
                channel.basic_ack(delivery_tag=method.delivery_tag)
                channel.stop_consuming()
                return
            try:
                if exchange and exchange_type == 'direct':
                    res = callback(method.routing_key, body)
                else:
                    res = callback(body)
                channel.basic_ack(delivery_tag=method.delivery_tag)
            except Exception:
                channel.basic_nack(delivery_tag=method.delivery_tag)
                raise

        for queue in queues:
            self.channel.basic_consume(queue=queue, auto_ack=False, on_message_callback=wrapper)
        self.channel.start_consuming()

    def publish(self, data, exchange='', queue=''):
        if not exchange and not queue:
            return  # TODO: handle this case

        self.channel.basic_publish(exchange, queue, data)

    def stop_consuming(self):
        self.channel.stop_consuming()
