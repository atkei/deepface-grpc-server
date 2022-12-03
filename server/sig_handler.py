import signal

from logger_factory import LoggerFactory

logger = LoggerFactory.get_logger(__name__)


class SignalHandler:
    KEEP_PROCESSING = True

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        logger.info("Handled signal: %s. Exiting gracefully" % signum)
        self.KEEP_PROCESSING = False
