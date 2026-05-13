"""Smart Guardian - Dashboard Stats Service"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.models.user import User
from app.models.alert import Alert
from app.models.sensor_data import SensorData
from app.models.notification import Notification

logger = logging.getLogger("smart-guardian")


class DashboardService:
    """Service for computing dashboard statistics"""

    def __init__(self, db: Session):
        self.db = db

    def get_admin_stats(self) -> Dict[str, Any]:
        """Get global admin dashboard statistics"""
        total_users = self.db.query(func.count(User.id)).scalar() or 0
        active_users = self.db.query(func.count(User.id)).filter(User.is_active == True).scalar() or 0
        total_alerts = self.db.query(func.count(Alert.id)).scalar() or 0
        critical_alerts = self.db.query(func.count(Alert.id)).filter(Alert.severity == "critical", Alert.is_resolved == False).scalar() or 0
        total_sensors = self.db.query(func.count(SensorData.id)).scalar() or 0
        unresolved_alerts = self.db.query(func.count(Alert.id)).filter(Alert.is_resolved == False).scalar() or 0

        return {
            "users": {"total": total_users, "active": active_users},
            "alerts": {"total": total_alerts, "critical": critical_alerts, "unresolved": unresolved_alerts},
            "sensor_readings": total_sensors,
            "timestamp": datetime.now().isoformat(),
        }

    def get_patient_stats(self, user_id: int) -> Dict[str, Any]:
        """Get patient-specific dashboard statistics"""
        total_alerts = self.db.query(func.count(Alert.id)).filter(Alert.user_id == user_id).scalar() or 0
        unread_alerts = self.db.query(func.count(Alert.id)).filter(Alert.user_id == user_id, Alert.is_read == False).scalar() or 0
        critical_alerts = self.db.query(func.count(Alert.id)).filter(Alert.user_id == user_id, Alert.severity == "critical").scalar() or 0
        total_sensors = self.db.query(func.count(SensorData.id)).filter(SensorData.user_id == user_id).scalar() or 0
        unread_notifications = self.db.query(func.count(Notification.id)).filter(Notification.user_id == user_id, Notification.is_read == False).scalar() or 0

        return {
            "user_id": user_id,
            "alerts": {"total": total_alerts, "unread": unread_alerts, "critical": critical_alerts},
            "sensor_readings": total_sensors,
            "unread_notifications": unread_notifications,
            "timestamp": datetime.now().isoformat(),
        }

    def get_alert_trend(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get alert count trend over the last N days"""
        start_date = datetime.now() - timedelta(days=days)
        results = (
            self.db.query(
                func.date(Alert.created_at).label("date"),
                func.count(Alert.id).label("total"),
                func.count(Alert.id).filter(Alert.severity == "critical").label("critical"),
            )
            .filter(Alert.created_at >= start_date)
            .group_by(func.date(Alert.created_at))
            .order_by(func.date(Alert.created_at))
            .all()
        )
        return [{"date": str(r.date), "total": r.total, "critical": r.critical} for r in results]

    def get_patient_alert_trend(self, user_id: int, days: int = 30) -> List[Dict[str, Any]]:
        """Get alert trend for a specific patient"""
        start_date = datetime.now() - timedelta(days=days)
        results = (
            self.db.query(
                func.date(Alert.created_at).label("date"),
                func.count(Alert.id).label("total"),
                func.count(Alert.id).filter(Alert.severity == "critical").label("critical"),
            )
            .filter(Alert.user_id == user_id, Alert.created_at >= start_date)
            .group_by(func.date(Alert.created_at))
            .order_by(func.date(Alert.created_at))
            .all()
        )
        return [{"date": str(r.date), "total": r.total, "critical": r.critical} for r in results]

    def get_severity_distribution(self, user_id: Optional[int] = None) -> Dict[str, int]:
        """Get alert distribution by severity"""
        query = self.db.query(Alert.severity, func.count(Alert.id))
        if user_id:
            query = query.filter(Alert.user_id == user_id)
        results = query.group_by(Alert.severity).all()
        return {severity: count for severity, count in results}
