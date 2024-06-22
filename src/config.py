from pydantic import MongoDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=True,
    )

    PROJECT_NAME: str = "FastAPI Mongo CRUD Example"
    SERVER_HOST: str = "http://localhost"

    MONGO_DATABASE_NAME: str = "items"
    MONGO_URI: MongoDsn

    SQLALCHEMY_DATABASE_URL: str


settings = Settings()  # type: ignore
