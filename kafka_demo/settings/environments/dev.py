from kafka_demo.settings.environments.base import Settings


class DevSettings(Settings):
    """Development settings."""

    HOST = "127.0.0.1"
    PORT = 8000
    # quantity of workers for uvicorn
    WORKERS_COUNT = 1
    # Enable uvicorn reloading
    RELOAD = True
    DB_HOST = "localhost"
    DB_PORT = 5432
    DB_USER = "postgres"
    DB_PASS = "postgres"
    DB_BASE = "postgres"
    DB_ECHO = False

    # Kafka
    BOOTSTRAP_SERVERS: list[str] = ["localhost:9093"]

    class Config(Settings.Config):
        env_file = ".env"
