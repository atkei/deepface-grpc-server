from face_service import FaceService
from logger_factory import LoggerFactory

import grpc
import asyncio
import face_pb2_grpc
from config import ServerConfig
from db_pool import start_pool, close_pool
from feature_mngr import FeatureManager
from sig_handler import SignalHandler

logger = LoggerFactory.get_logger(__name__)


async def serve():
    cfg = ServerConfig.get_instance()
    logger.info("Loaded server config: %s" % cfg)
    await start_pool()

    feature_mngr = FeatureManager()
    face_service = FaceService(cfg, feature_mngr)

    server = grpc.aio.server()
    face_pb2_grpc.add_FaceServiceServicer_to_server(face_service, server)
    listen_addr = '[::]:{}'.format(cfg.listen_port)
    server.add_insecure_port(listen_addr)

    await server.start()
    logger.info("Started server on %s" % listen_addr)

    sig_handler = SignalHandler()
    sync_tmpl_task = asyncio.create_task(feature_mngr.sync_features(sig_handler))
    pool_close_task = asyncio.create_task(close_pool(sig_handler))
    await sync_tmpl_task
    await pool_close_task

    await server.wait_for_termination(3)
    logger.info("Exited")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(serve())
