"""Smart Guardian - Analytics Service (Seizure Patterns)"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, extract
from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.models.sensor_data import SensorData

logger = logging.getLogger("smart-guardian")


class AnalyticsService:
    """Service for seizure pattern analysis and analytics"""

    def __init__(self, db: Session):
        self.db = db

    def get_seizure_frequency(self, user_id: int, days: int = 90) -> Dict[str, Any]:
        """Get seizure frequency stats over a period"""
        start_date = datetime.now() - timedelta(days=days)
        total = self.db.query(func.count(Alert.id)).filter(
            Alert.user_id == user_id, Alert.alert_type == "seizure_detection", Alert.created_at >= start_date
        ).scalar() or 0

        daily_avg = round(total / max(days, 1), 2)
        weekly_avg = round(total / max(days / 7, 1), 2)
        monthly_avg = round(total / max(days / 30, 1), 2)

        return {
            "user_id": user_id,
            "period_days": days,
            "total_seizures": total,
            "daily_average": daily_avg,
            "weekly_average": weekly_avg,
            "monthly_average": monthly_avg,
        }

    def get_hourly_distribution(self, user_id: int, days: int = 90) -> List[Dict[str, Any]]:
        """Get seizure distribution by hour of day"""
        start_date = datetime.now() - timedelta(days=days)
        results = (
            self.db.query(
                extract("hour", Alert.created_at).label("hour"),
                func.count(Alert.id).label("count"),
            )
            .filter(Alert.user_id == user_id, Alert.alert_type == "seizure_detection", Alert.created_at >= start_date)
            .group_by(extract("hour", Alert.created_at))
            .order_by(extract("hour", Alert.created_at))
            .all()
        )
        return [{"hour": int(r.hour), "count": r.count} for r in results]

    def get_weekly_distribution(self, user_id: int, days: int = 180) -> List[Dict[str, Any]]:
        """Get seizure distribution by day of week"""
        start_date = datetime.now() - timedelta(days=days)
        results = (
            self.db.query(
                extract("dow", Alert.created_at).label("day_of_week"),
                func.count(Alert.id).label("count"),
            )
            .filter(Alert.user_id == user_id, Alert.alert_type == "seizure_detection", Alert.created_at >= start_date)
            .group_by(extract("dow", Alert.created_at))
            .order_by(extract("dow", Alert.created_at))
            .all()
        )
        day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
        return [{"day": day_names[int(r.day_of_week)], "day_index": int(r.day_of_week), "count": r.count} for r in results]

    def get_vitals_during_seizures(self, user_id: int, limit: int = 20) -> List[Dict[str, Any]]:
        """Get vitals data recorded during seizure alerts"""
        alerts = (
            self.db.query(Alert)
            .filter(Alert.user_id == user_id, Alert.alert_type == "seizure_detection")
            .order_by(Alert.created_at.desc())
            .limit(limit)
            .all()
        )
        return [{
            "alert_id": a.id,
            "severity": a.severity,
            "confidence": a.confidence,
            "heart_rate": a.heart_rate,
            "spo2": a.spo2,
            "created_at": a.created_at.isoformat(),
        } for a in alerts]

    def get_seizure_summary(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive seizure analytics summary"""
        frequency = self.get_seizure_frequency(user_id)
        hourly = self.get_hourly_distribution(user_id)
        weekly = self.get_weekly_distribution(user_id)
        vitals = self.get_vitals_during_seizures(user_id, limit=10)

        peak_hour = max(hourly, key=lambda x: x["count"])["hour"] if hourly else None
        peak_day = max(weekly, key=lambda x: x["count"])["day"] if weekly else None

        avg_hr = None
        avg_spo2 = None
        if vitals:
            hr_values = [v["heart_rate"] for v in vitals if v["heart_rate"] is not None]
            spo2_values = [v["spo2"] for v in vitals if v["spo2"] is not None]
            if hr_values:
                avg_hr = round(sum(hr_values) / len(hr_values), 1)
            if spo2_values:
                avg_spo2 = round(sum(spo2_values) / len(spo2_values), 1)

        return {
            "user_id": user_id,
            "frequency": frequency,
            "peak_hour": peak_hour,
            "peak_day": peak_day,
            "avg_heart_rate_during_seizure": avg_hr,
            "avg_spo2_during_seizure": avg_spo2,
            "recent_seizure_vitals": vitals,
        }
