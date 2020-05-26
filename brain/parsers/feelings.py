from brain.utils.common import get_logger

logger = get_logger(__name__)


class FeelingParser:
    field = 'feelings'

    def parse(self, data, context):
        logger.info(f'running feelings parser')
        return data
