from brain.utils.common import get_logger

logger = get_logger(__name__)


class FeelingParser:
    """
    Parse feelings.
    """

    field = 'feelings'

    def parse(self, data, context):
        """
        Parse feelings. Currently there is no what to parse, as the result is already in the right format.

        :param data: the data to parse.
        :param context: passed by the parsers context.
        :return: the given data.
        """

        logger.info(f'running feelings parser')
        return data
