from enum import StrEnum
from pathlib import Path

from pydantic import Field, PostgresDsn, RedisDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    STAGING = "staging"
    TESTING = "testing"


class LogLevel(StrEnum):
    TRACE = "TRACE"
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class Settings(BaseSettings):
    # Project Environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # Frontend
    FRONTEND_BASE_URL: str = "http://localhost:3000"

    # CORS
    CORS_ORIGINS: str = "*"
    CORS_ALLOW_CREDENTIALS: bool = False

    # JWT
    JWT_SECRET: str = "secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    JWT_REFRESH_TOKEN_EXPIRE_MINUTES: int = 10_080

    # Database
    POSTGRES_HOST: str = Field("postgres", description="Postgres host")
    POSTGRES_PORT: int = Field(5432, description="Postgres port")
    POSTGRES_DB: str = Field("fastapi-ecommerce-Database", description="Databse name")
    POSTGRES_USER: str = Field("postgres", description="Database user")
    POSTGRES_PASSWORD: str = Field("postgres", description="Database password")
    DB_POOL_SIZE: int = Field(5, description="Number of connections to maintain in the pool")
    DB_MAX_OVERFLOW: int = Field(10, description="MAX connections beyond pool_size")
    DB_POOL_RECYCLE: int = Field(
        3600, description="Recycle connections after N seconds (1 hour default)"
    )
    DB_POOL_PRE_PING: bool = Field(
        True, description="Verify connection health before using from pool"
    )
    DB_ECHO: bool = Field(False, description="Log all SQL statements")

    # Redis
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = ""

    # Caching
    CACHING_PREFIX: str = "fastapi-cache"
    CACHING_DEFAULT_TTL: int = 300  # seconds (5 min)

    # Rate Limit
    RATE_LIMIT_DEFAULT: str = "100/minute"

    # Log
    LOG_LEVEL: LogLevel = LogLevel.INFO
    LOG_DIR: Path = Path("logs")
    LOG_JSON: bool = True
    LOG_TO_FILE: bool = True
    LOG_ROTATION: str = Field("1 week", description="Log rotation interval")
    LOG_RETENTION: str = Field("1 month", description="Log retention period")
    LOG_COMPRESSION: str | None = Field(None, description="Log compression (e.g. zip, gz, tar)")

    # SMTP
    SMTP_SERVER: str = "YOUR_SMTP_SERVER"
    SMTP_PORT: int = 587
    SMTP_LOGIN: str = "YOUR_SMTP_LOGIN"
    SMTP_KEY: str = "YOUR_SMTP_KEY"
    SMTP_FROM_NAME: str = "open-vendor"
    SMTP_FROM: str = "open_vendor@gmail.com"

    # Google
    GOOGLE_CLIENT_SECRET: str = "YOUR_GOOGLE_CLIENT_SECRET"
    GOOGLE_CLIENT_ID: str = "YOUR_GOOGLE_CLIENT_ID"

    # Facebook
    FACEBOOK_APP_ID: str = "YOUR_FACEBOOK_APP_ID"
    FACEBOOK_APP_SECRET: str = "YOUR_FACEBOOK_APP_SECRET"

    @computed_field
    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    @computed_field
    @property
    def REDIS_URL(self) -> RedisDsn:
        return RedisDsn.build(
            scheme="redis", host=self.REDIS_HOST, port=self.REDIS_PORT, password=self.REDIS_PASSWORD
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings: Settings = Settings()  # type: ignore
