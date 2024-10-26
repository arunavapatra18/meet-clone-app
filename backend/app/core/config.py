from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, computed_field


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env", env_ignore_empty=True, extra="ignore"
    )

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432

    @computed_field
    @property
    def POSTGRES_DB_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )

    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()
