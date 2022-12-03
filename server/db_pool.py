import asyncio

from piccolo.engine import engine_finder

from config import DbConfig
from logger_factory import LoggerFactory
from sig_handler import SignalHandler

logger = LoggerFactory.get_logger(__name__)


async def start_pool():
    engine = engine_finder()
    pool_size = DbConfig.get_instance().max_pool_size
    await engine.start_connection_pool(max_size=pool_size)
    logger.info("Stated db connection pool (max size=%s)" % pool_size)


async def close_pool(handler: SignalHandler):
    while handler.KEEP_PROCESSING:
        await asyncio.sleep(0.1)
    engine = engine_finder()
    await engine.close_connection_pool()
    logger.info("Closed db connection pool")
