"""Smart Guardian Epilepsy AI - Backend FastAPI"""

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.logging import setup_logging
from app.core.mqtt_client import mqtt_client
from app.services.model_service import model_service
from app.api.auth_routes import router as auth_router
from app.api.user_routes import router as user_router
from app.api.sensor_routes import router as sensor_router
from app.api.alert_routes import router as alert_router
from app.api.prediction_routes import router as prediction_router
from app.api.notification_routes import router as notification_router
from app.api.dashboard_routes import router as dashboard_router
import logging

logger = logging.getLogger("smart-guardian")


def handle_sensor_message(topic: str, payload: dict):
    """Handle incoming MQTT sensor messages"""
    logger.info("Sensor data received on %s", topic)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events"""
    setup_logging()
    logger.info("Starting %s v%s", settings.APP_NAME, settings.APP_VERSION)
    model_service.load_model()
    logger.info("AI model loaded: %s", model_service.is_loaded)
    mqtt_client.register_handler(settings.MQTT_TOPIC_SENSORS, handle_sensor_message)
    mqtt_client.connect()
    logger.info("MQTT client connected")
    yield
    mqtt_client.disconnect()
    logger.info("Shutting down %s", settings.APP_NAME)


app = FastAPI(
    title=settings.APP_NAME,
    description="API Backend pour la surveillance de crises depilepsie",
    version=settings.APP_VERSION,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(sensor_router)
app.include_router(alert_router)
app.include_router(prediction_router)
app.include_router(notification_router)
app.include_router(dashboard_router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Smart Guardian Epilepsy AI API",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/api/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "smart-guardian-backend",
        "version": settings.APP_VERSION,
    }


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
