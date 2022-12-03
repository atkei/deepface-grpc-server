import os
from dataclasses import dataclass
from env_vars import EnvironmentVariables as env
from enums import SimilarityMetricsType, LogLevel, FeatureModel, DetectorBackend


@dataclass(frozen=True)
class ServerConfig:
    listen_port: int
    log_level: LogLevel
    similarity_metrics: SimilarityMetricsType
    similarity_threshold: float
    feature_model: FeatureModel
    detector_backend: DetectorBackend

    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(ServerConfig, cls).__new__(cls)
        return cls._instance

    def __post_init__(self):
        if type(self.listen_port) is not int or self.listen_port < 0 or self.listen_port > 65535:
            raise ValueError("Invalid listen port: " + self.listen_port)
        if type(self.similarity_threshold) is not float or self.similarity_threshold < 0:
            raise ValueError("Invalid similarity threshold: " + self.similarity_threshold)

    @staticmethod
    def get_instance():
        return ServerConfig(
            listen_port=int(os.environ.get(env.listen_port.key, env.listen_port.default)),
            log_level=LogLevel.of(os.environ.get(env.log_level.key, env.log_level.default)),
            similarity_metrics=SimilarityMetricsType.of(os.environ.get(env.sim_metrics.key, env.sim_metrics.default)),
            similarity_threshold=float(os.environ.get(env.sim_threshold.key, env.sim_threshold.default)),
            feature_model=FeatureModel.of(os.environ.get(env.tmpl_model.key, env.tmpl_model.default)),
            detector_backend=DetectorBackend.of(os.environ.get(env.detect_backend.key, env.detect_backend.default))
        )


@dataclass(frozen=True)
class DbConfig:
    database: str
    user: str
    password: str
    host: str
    port: str
    max_pool_size: int

    def __new__(cls, *args, **kargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super(DbConfig, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def get_instance():
        return DbConfig(
            database=os.environ.get(env.database.key, env.database.default),
            user=os.environ.get(env.db_user.key, env.db_user.default),
            password=os.environ.get(env.db_pass.key, env.db_pass.default),
            host=os.environ.get(env.db_host.key, env.db_host.default),
            port=os.environ.get(env.db_port.key, env.db_port.default),
            max_pool_size=int(os.environ.get(env.db_max_pool_size.key, env.db_max_pool_size.default))
        )
