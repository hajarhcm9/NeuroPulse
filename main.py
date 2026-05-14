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
from app.api.export_routes import router as export_router
from app.core.mqtt_subscriber import setup_mqtt_subscriber
from app.core.rate_limiter import RateLimitMiddleware, SecurityHeadersMiddleware
from app.core.device_auth import device_auth
from app.core.audit_logger import audit
from app.api.websocket_routes import router as websocket_router, ws_manager
from app.api.training_routes import router as training_router
import logging
import asyncio

logger = logging.getLogger("smart-guardian")



@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: startup and shutdown events"""
    setup_logging()
    logger.info("Starting %s v%s", settings.app_name, settings.app_version)
    model_service.load_model()
    logger.info("AI model loaded: %s", model_service.is_loaded)
    device_auth.register_device("SG-BRACELET-001", "sg-key-dev-001")
    device_auth.register_device("SG-BRACELET-002", "sg-key-dev-002")
    logger.info("Registered %d default devices", len(device_auth._devices))
    setup_mqtt_subscriber()
    mqtt_client.connect()
    ws_manager.set_loop(asyncio.get_event_loop())
    logger.info("MQTT client connected")
    yield
    mqtt_client.disconnect()
    logger.info("Shutting down %s", settings.app_name)


app = FastAPI(
    title=settings.app_name,
    description="API Backend pour la surveillance de crises depilepsie",
    version=settings.app_version,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware, requests_per_minute=60)
app.add_middleware(SecurityHeadersMiddleware)

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(sensor_router)
app.include_router(alert_router)
app.include_router(prediction_router)
app.include_router(notification_router)
app.include_router(dashboard_router)
app.include_router(export_router)
app.include_router(websocket_router)
app.include_router(training_router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Welcome to Smart Guardian Epilepsy AI API",
        "version": settings.app_version,
        "status": "running",
        "docs": "/api/docs",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "smart-guardian-backend",
        "version": settings.app_version,
    }



@app.post("/api/test/predict")
async def test_predict(body: dict):
    features = body.get("features", [])
    from app.services.model_service import model_service
    import numpy as np
    return model_service.predict(np.array(features))
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )
