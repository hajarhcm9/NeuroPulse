"""Smart Guardian - MQTT subscriber for real-time seizure detection."""

import logging
import math
import time
from typing import Dict
from app.core.mqtt_client import mqtt_client
from app.core.config import settings
from app.services.sensor_model import sensor_model

logger = logging.getLogger("smart-guardian")

_last_alert_time: Dict[int, float] = {}
ALERT_COOLDOWN_SECONDS = 30
CRITICAL_THRESHOLD = 0.8
WARNING_THRESHOLD = 0.5


def _sensor_handler(topic: str, payload: dict):
    """Handle incoming MQTT sensor data: store + predict + alert."""
    from app.core.database import SessionLocal
    from app.services.sensor_service import SensorService
    from app.services.alert_service import AlertService
    from app.services.notification_service import NotificationService
    from app.schemas.alert import AlertCreate
    from app.schemas.notification import NotificationCreate
    from app.schemas.sensor_data import SensorDataCreate

    user_id = payload.get("user_id")
    device_id = payload.get("device_id", "unknown")

    db = SessionLocal()
    try:
        # 1) Store raw sensor data
        try:
            store_payload = dict(payload)
            if "sensor_type" not in store_payload:
                store_payload["sensor_type"] = "wearable"
            sensor_svc = SensorService(db)
            sensor_data = SensorDataCreate(**store_payload)
            sensor_svc.store_sensor_data(sensor_data)
        except Exception as e:
            logger.error("Sensor store failed: %s", e)

        # 2) Extract features for prediction
        ax = float(payload.get("accelerometer_x", 0) or 0)
        ay = float(payload.get("accelerometer_y", 0) or 0)
        az = float(payload.get("accelerometer_z", 0) or 0)
        accel_mag = math.sqrt(ax * ax + ay * ay + az * az)

        features = {
            "heart_rate": float(payload.get("heart_rate", 75) or 75),
            "spo2": float(payload.get("spo2", 98) or 98),
            "accelerometer": round(accel_mag, 3),
            "emg_signal": float(payload.get("emg_signal", 0.3) or 0.3),
            "eda_signal": float(payload.get("eda_signal", 0.3) or 0.3),
            "temperature": float(payload.get("temperature", 36.5) or 36.5),
        }

        # 3) Run prediction
        result = sensor_model.predict(features)
        prob = result["seizure_probability"]
        is_seizure = result["is_seizure"]
        risk_factors = result.get("risk_factors", [])

        logger.info(
            "MQTT predict: user=%s device=%s prob=%.4f seizure=%s",
            user_id, device_id, prob, is_seizure,
        )

        # 4) Alert if seizure detected
        if is_seizure and user_id:
            now = time.time()
            last = _last_alert_time.get(user_id, 0)
            if now - last < ALERT_COOLDOWN_SECONDS:
                logger.debug("Alert cooldown active for user %s", user_id)
                return
            _last_alert_time[user_id] = now

            severity = "critical" if prob >= CRITICAL_THRESHOLD else "warning"
            factors_str = ", ".join(risk_factors) if risk_factors else "Abnormal sensor pattern"
            message = "Seizure risk p=" + str(round(prob, 2)) + ": " + factors_str

            try:
                alert_svc = AlertService(db)
                alert = alert_svc.create_alert(AlertCreate(
                    user_id=user_id,
                    device_id=device_id,
                    alert_type="seizure_detection",
                    severity=severity,
                    confidence=prob,
                    heart_rate=features.get("heart_rate"),
                    spo2=features.get("spo2"),
                    message=message,
                ))

                notif_svc = NotificationService(db)

                # Always create in-app notification
                notif_svc.create_notification(NotificationCreate(
                    user_id=user_id,
                    alert_id=alert.id,
                    channel="in_app",
                    title="Seizure Alert",
                    body=message,
                ))

                # Critical alerts also get email + push
                if severity == "critical":
                    notif_svc.create_notification(NotificationCreate(
                        user_id=user_id,
                        alert_id=alert.id,
                        channel="email",
                        title="URGENT: Seizure Alert",
                        body=message,
                    ))
                    notif_svc.create_notification(NotificationCreate(
                        user_id=user_id,
                        alert_id=alert.id,
                        channel="push",
                        title="Seizure Alert",
                        body=message,
                    ))

                logger.warning(
                    "Alert created: user=%s severity=%s prob=%.4f",
                    user_id, severity, prob,
                )
            except Exception as e:
                logger.error("Alert/notification creation failed: %s", e)

    finally:
        db.close()


def setup_mqtt_subscriber():
    """Register the MQTT sensor handler. Called at app startup."""
    mqtt_client.register_handler(settings.mqtt_topic_sensors, _sensor_handler)
    logger.info("MQTT sensor subscriber registered on topic: %s", settings.mqtt_topic_sensors)