from loguru import logger


class Exception(Exception):

    def __init__(self, message):
        super().__init__(message)
        logger.exception(message)


class TypeError(Exception):

    def __init__(self, message):
        super().__init__(message)
        logger.error(message)

class StopExecution(Exception):

    def __init__(self):
        super().__init__("停止执行程序")
