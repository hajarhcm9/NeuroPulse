"""Smart Guardian - Alert service"""

import logging
from typing import List
from fastapi import HTTPException, status
from app.core.mqtt_client import mqtt_client
from app.core.config import settings
from app.models.alert import Alert
from app.repositories.alert_repository import AlertRepository
from app.schemas.alert import AlertCreate, AlertResponse, AlertUpdate

logger = logging.getLogger("smart-guardian")


class AlertService:
    """Business logic for alerts"""

    def __init__(self, db):
        self.alert_repo = AlertRepository(db)

    def create_alert(self, data: AlertCreate) -> AlertResponse:
        alert = Alert(
            user_id=data.user_id,
            device_id=data.device_id,
            alert_type=data.alert_type,
            severity=data.severity,
            confidence=data.confidence,
            heart_rate=data.heart_rate,
            spo2=data.spo2,
            message=data.message,
        )
        alert = self.alert_repo.create(alert)
        mqtt_client.publish(settings.MQTT_TOPIC_ALERTS, AlertResponse.model_validate(alert).model_dump())
        logger.warning("Alert created: type=%s severity=%s user=%s", data.alert_type, data.severity, data.user_id)
        return AlertResponse.model_validate(alert)

    def get_user_alerts(self, user_id: int, limit: int = 50) -> List[AlertResponse]:
        alerts = self.alert_repo.get_by_user(user_id, limit)
        return [AlertResponse.model_validate(a) for a in alerts]

    def get_unread(self, user_id: int) -> List[AlertResponse]:
        alerts = self.alert_repo.get_unread_by_user(user_id)
        return [AlertResponse.model_validate(a) for a in alerts]

    def get_critical(self, limit: int = 50) -> List[AlertResponse]:
        alerts = self.alert_repo.get_critical_alerts(limit)
        return [AlertResponse.model_validate(a) for a in alerts]

    def update_alert(self, alert_id: int, data: AlertUpdate) -> AlertResponse:
        alert = self.alert_repo.get_by_id(alert_id)
        if not alert:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found")
        if data.is_read is not None:
            alert.is_read = data.is_read
        if data.is_resolved is not None:
            alert.is_resolved = data.is_resolved
        alert = self.alert_repo.update(alert)
        return AlertResponse.model_validate(alert)
