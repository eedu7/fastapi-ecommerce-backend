from enum import StrEnum

from pydantic import Field, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(StrEnum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    STAGING = "staging"
    TESTING = "testing"


class Settings(BaseSettings):
    # Project Environment
    ENVIRONMENT: Environment = Environment.DEVELOPMENT

    # Database
    DB_HOST: str = Field("postgres", description="Postgres host")
    DB_PORT: int = Field(5432, description="Postgres port")
    DB_NAME: str = Field("fastapi-ecommerce-Database", description="Databse name")
    DB_USER: str = Field("postgres", description="Database user")
    DB_PASSWORD: str = Field("postgres", description="Database password")
    DB_POOL_SIZE: int = Field(
        5, description="Number of connections to maintain in the pool"
    )
    DB_MAX_OVERFLOW: int = Field(10, description="MAX connections beyond pool_size")
    DB_POOL_RECYCLE: int = Field(
        3600, description="Recycle connections after N seconds (1 hour default)"
    )
    DB_POOL_PRE_PING: bool = Field(
        True, description="Verify connection health before using from pool"
    )
    DB_ECHO: bool = Field(False, description="Log all SQL statements")

    @computed_field
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            path=f"/{self.DB_NAME}",
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


settings: Settings = Settings()
