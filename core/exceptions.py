import traceback

from loguru import logger


class Exception(Exception):

    def __init__(self, message):
        super().__init__(message)
        logger.error(message)
        logger.debug(traceback.format_exc())

class TypeError(Exception):

    def __init__(self, message):
        super().__init__(message)
        logger.error(message)
