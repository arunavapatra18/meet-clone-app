from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, computed_field

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../../.env",
        env_ignore_empty=True,
        extra="ignore"
    )

    POSTGRES_INDEXES_NAMING_CONVENTION: dict = {
    "ix": "%(column_0_label)s_idx",
    "uq": "%(table_name)s_%(column_0_name)s_key",
    "ck": "%(table_name)s_%(constraint_name)s_check",
    "fk": "%(table_name)s_%(column_0_name)s_fkey",
    "pk": "%(table_name)s_pkey",
}

    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432

    @computed_field
    @property
    def POSTGRES_DB_URI(self) -> PostgresDsn: 
        # print(self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_SERVER, self.POSTGRES_PORT, self.POSTGRES_DB)
        return MultiHostUrl.build(
        scheme="postgresql+psycopg2",
        username = self.POSTGRES_USER,
        password = self.POSTGRES_PASSWORD,
        host = self.POSTGRES_SERVER,
        port = self.POSTGRES_PORT,
        path = self.POSTGRES_DB
    )

settings = Settings()
