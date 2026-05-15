"""Smart Guardian - Application Configuration"""

from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "Smart Guardian"
    app_version: str = "1.0.0"
    app_description: str = "Epilepsy monitoring and seizure detection backend"
    environment: str = "development"
    debug: bool = True

    # Server
    host: str = "0.0.0.0"
    port: int = 8000

    # CORS
    cors_origins: List[str] = ["http://localhost:3000"]

    # PostgreSQL
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_db: str = "smartguardian"
    postgres_user: str = "sgadmin"
    postgres_password: str = "sgpass123"
    database_url: str = ""
    database_pool_size: int = 5
    database_max_overflow: int = 10

    # JWT / Security
    jwt_secret_key: str = "change-me-to-a-secure-random-string-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_minutes: int = 1440
    secret_key: str = "change-me-to-a-secure-random-string-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440
    refresh_token_expire_days: int = 7

    # MQTT
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_username: str = ""
    mqtt_password: str = ""
    mqtt_keepalive: int = 60
    mqtt_topic_prefix: str = "smart-guardian"
    mqtt_broker_host: str = "localhost"
    mqtt_broker_port: int = 1883
    mqtt_topic_sensors: str = "smart-guardian/sensors"
    mqtt_topic_alerts: str = "smart-guardian/alerts"

    # Model
    model_path: str = "models/seizure_detector.h5"
    model_version: str = "1.0.0"
    seizure_threshold: float = 0.5

    # Logging
    log_file: str = "logs/smart_guardian.log"
    log_level: str = "INFO"

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "allow",
    }


def _build_database_url(settings: Settings) -> str:
    """Build PostgreSQL connection URL from components."""
    if settings.database_url:
        return settings.database_url
    return (
        f"postgresql://{settings.postgres_user}:{settings.postgres_password}"
        f"@{settings.postgres_host}:{settings.postgres_port}/{settings.postgres_db}"
    )


settings = Settings()
settings.database_url = _build_database_url(settings)
