import time

import pika
from furl import furl

from brain.utils.common import get_logger

logger = get_logger(__name__)


class RabbitMQ:
    def __init__(self, url):
        logger.info(f'initializing rabbitmq connection: {url=}')
        self.url = url
        _url = furl(url)
        host, port = _url.host, _url.port
        self.connection = self.connect(host, port)
        self.channel = self.connection.channel()

    @classmethod
    def connect(cls, host, port, max_retries=15, sleep=1):
        logger.info(f'trying to connect rabbitmq: {host=}, {port=}, {max_retries=}, {sleep=}')
        last_error = None  # type: Exception
        for i in range(max_retries):
            try:
                conn = pika.BlockingConnection(pika.ConnectionParameters(host=host, port=port))
                return conn
            except pika.connection.exceptions.AMQPError as error:
                last_error = error
                logger.info(f'exception while trying to connect: {error}, waiting {sleep} seconds before retrying')
                print(f'Exception while trying to connect: {error}, waiting {sleep} seconds before retrying')
                time.sleep(sleep)
        logger.error('failed to connect rabbitmq, reached max retries')
        raise last_error

    def close(self):
        logger.info(f'closing connection')
        self.channel.close()
        self.connection.close()

    def consume(self, callback, exchange, queues, exchange_type='fanout'):
        logger.info(f'preparing to consuming mq: {callback=}, {exchange=}, {queues=}, {exchange_type=}')
        if exchange:
            self.channel.exchange_declare(exchange=exchange, exchange_type=exchange_type)
        for queue in queues:
            self.channel.queue_declare(queue=queue)
            if exchange:
                self.channel.queue_bind(exchange=exchange, queue=queue)

        def wrapper(channel, method, properties, body):
            try:
                if exchange and exchange_type == 'direct':
                    res = callback(method.routing_key, body)
                else:
                    res = callback(body)
                channel.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as error:
                logger.error(f'exception in consume callback: {error}')
                channel.basic_nack(delivery_tag=method.delivery_tag)
                res = None
            return res

        for queue in queues:
            self.channel.basic_consume(queue=queue, auto_ack=False, on_message_callback=wrapper)
        logger.info(f'starting to consume mq')
        self.channel.start_consuming()

    def publish(self, data, exchange='', queue=''):
        if not exchange and not queue:
            logger.error(f'queue or exchange were not given')
            raise Exception('Queue or exchange were not given')
        logger.debug(f'publishing to mq: {exchange=}, {queue=}')
        self.channel.basic_publish(exchange, queue, data)
