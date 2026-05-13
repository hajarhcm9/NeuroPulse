"""Smart Guardian Epilepsy AI - Configuration centrale"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    APP_NAME: str = "Smart Guardian Epilepsy AI"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/smart_guardian"
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10

    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8080"]

    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_USERNAME: str = ""
    MQTT_PASSWORD: str = ""
    MQTT_TOPIC_SENSORS: str = "smart-guardian/sensors/#"
    MQTT_TOPIC_ALERTS: str = "smart-guardian/alerts"

    AI_SEIZURE_THRESHOLD: float = 0.5
    AI_MODEL_PATH: str = "models/seizure_detector.h5"
    AI_CONFIDENCE_THRESHOLD: float = 0.85

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"


settings = Settings()