from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine

from config import DbConfig
from logger_factory import LoggerFactory

logger = LoggerFactory.get_logger(__name__)
cfg = DbConfig.get_instance()
logger.info("Loaded db config: %s" % cfg)

DB = PostgresEngine(config={
    "database": cfg.database,
    "user": cfg.user,
    "password": cfg.password,
    "host": cfg.host,
    "port": cfg.port
})


# A list of paths to piccolo apps
# e.g. ['blog.piccolo_app']
APP_REGISTRY = AppRegistry(apps=["db.piccolo_app"])
