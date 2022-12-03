import sys
from logging import Formatter, getLogger, StreamHandler, INFO, Logger, DEBUG

from enums import LogLevel
from config import ServerConfig


class LoggerFactory:
    @staticmethod
    def get_logger(module: str) -> Logger:
        formatter = Formatter('%(asctime)s %(levelname)5s [%(thread)s] %(name)s:%(lineno)s - %(message)s')
        log_level = ServerConfig.get_instance().log_level

        logger = getLogger(module)
        handler = StreamHandler(sys.stdout)

        if log_level == LogLevel.DEBUG:
            logger.setLevel(DEBUG)
            handler.setLevel(DEBUG)
        else:
            logger.setLevel(INFO)
            handler.setLevel(INFO)

        handler.setFormatter(formatter)
        logger.addHandler(handler)

        return logger
