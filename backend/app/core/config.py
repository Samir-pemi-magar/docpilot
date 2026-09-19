from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "DocPilot API"
    app_version: str = "0.1.0"
    debug: bool = False
    minio_endpoint: str = "http://minio:9000"
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str = "documents"

    database_url: str
    qdrant_url: str = "http://qdrant:6333"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()