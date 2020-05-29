"""
The rabbitmq module provides an interface for rabbitmq.
"""

import time

import pika
from furl import furl

from brain.utils.common import get_logger

logger = get_logger(__name__)


class RabbitMQ:
    """
    The rabbitmq class connects to the MQ, and allows consuming and publishing to the MQ.

    :param url: address of the MQ.
    """

    def __init__(self, url: str):
        logger.info(f'initializing rabbitmq connection: {url=}')
        self.url = url
        _url = furl(url)
        host, port = _url.host, _url.port
        self.connection = self.connect(host, port)
        self.channel = self.connection.channel()

    @classmethod
    def connect(cls, host: str, port: int, max_retries: int = 15, sleep: int = 1) -> pika.BlockingConnection:
        """
        Connect to the MQ, retry several times until success, and raise exception after some failed retries.

        :param host: MQ hostname.
        :param port: MQ port number.
        :param max_retries: maximum number of retries to connect.
        :param sleep: time to sleep (in seconds) between each try.
        :return: the connection object.
        """

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
        """
        Close connection to the MQ.
        """

        logger.info(f'closing connection')
        self.channel.close()
        self.connection.close()

    def consume(self, callback: callable, exchange: str, queues: list, exchange_type: str = 'fanout'):
        """
        Consume the MQ.

        :param callback: will be called when consuming new message.
        :param exchange: exchange name (if '' will be ignored).
        :param queues: queues to consume.
        :param exchange_type: currently supported are 'fanout' and 'direct'
        """

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
        """
        Publish message to the MQ. Either exchange or queue must be provided.

        :param data: data to send.
        :param exchange: exchange name to publish data to.
        :param queue: queue to publish data to.
        """

        if not exchange and not queue:
            logger.error(f'queue or exchange were not given')
            raise Exception('Queue or exchange were not given')
        logger.debug(f'publishing to mq: {exchange=}, {queue=}')
        self.channel.basic_publish(exchange, queue, data)
