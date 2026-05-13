"""Smart Guardian - Alert repository"""

from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.alert import Alert


class AlertRepository:
    """Data access layer for Alert model"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, alert: Alert) -> Alert:
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def get_by_id(self, alert_id: int) -> Optional[Alert]:
        return self.db.query(Alert).filter(Alert.id == alert_id).first()

    def get_by_user(self, user_id: int, limit: int = 50) -> List[Alert]:
        return self.db.query(Alert).filter(Alert.user_id == user_id).order_by(Alert.created_at.desc()).limit(limit).all()

    def get_unread_by_user(self, user_id: int) -> List[Alert]:
        return self.db.query(Alert).filter(Alert.user_id == user_id, Alert.is_read == False).order_by(Alert.created_at.desc()).all()

    def get_critical_alerts(self, limit: int = 50) -> List[Alert]:
        return self.db.query(Alert).filter(Alert.severity == "critical", Alert.is_resolved == False).order_by(Alert.created_at.desc()).limit(limit).all()

    def update(self, alert: Alert) -> Alert:
        self.db.commit()
        self.db.refresh(alert)
        return alert
