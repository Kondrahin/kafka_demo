from enum import Enum
from pathlib import Path
from tempfile import gettempdir

from pydantic import BaseSettings, BaseConfig
from yarl import URL

TEMP_DIR = Path(gettempdir())


class AppEnvTypes(str, Enum):
    DEV: str = "dev"


class BaseAppSettings(BaseSettings):

    ENV_TYPE: AppEnvTypes = "dev"

    class Config:
        env_file = ".env"
        env_prefix = "APP_"


class Settings(BaseAppSettings):
    """Application settings."""

    HOST: str
    PORT: int
    # quantity of workers for uvicorn
    WORKERS_COUNT: int
    # Enable uvicorn reloading
    RELOAD: bool
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_BASE: str
    DB_ECHO: bool

    # Kafka
    BOOTSTRAP_SERVERS: list[str]

    @property
    def db_url(self) -> URL:
        """
        Assemble database URL from settings.

        :return: database URL.
        """
        return URL.build(
            scheme="postgresql+asyncpg",
            host=self.DB_HOST,
            port=self.DB_PORT,
            user=self.DB_USER,
            password=self.DB_PASS,
            path=f"/{self.DB_BASE}",
        )

    class Config:
        env_file = ".env"
        env_prefix = "APP_"
        env_file_encoding = "utf-8"

