class EnvironmentVariable:
    def __init__(self, key: str, default: str):
        self.key = key
        self.default = default


class EnvironmentVariables:
    listen_port = EnvironmentVariable("FACE_SERVICE_LISTEN_PORT", "50051")
    log_level = EnvironmentVariable("FACE_SERVICE_LOG_LEVEL", "INFO")
    sim_metrics = EnvironmentVariable("FACE_SERVICE_SIM_METRICS", "cosine")
    sim_threshold = EnvironmentVariable("FACE_SERVICE_SIM_THRESHOLD", "0.5")
    feat_model = EnvironmentVariable("FACE_SERVICE_FEATURE_MODEL", "Facenet")
    detect_backend = EnvironmentVariable("FACE_SERVICE_DETECT_BACKEND", "opencv")

    database = EnvironmentVariable("FACE_SERVICE_DB_NAME", "face_db")
    db_user = EnvironmentVariable("FACE_SERVICE_DB_USER", "postgres")
    db_pass = EnvironmentVariable("FACE_SERVICE_DB_PASS", "postgres")
    db_host = EnvironmentVariable("FACE_SERVICE_DB_HOST", "localhost")
    db_port = EnvironmentVariable("FACE_SERVICE_DB_PORT", "35432")
    db_max_pool_size = EnvironmentVariable("FACE_SERVICE_DB_MAX_POOL_SIZE", "20")
