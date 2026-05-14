"""Smart Guardian - Prediction analytics and model performance tracking."""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.models.sensor_data import SensorData

logger = logging.getLogger("smart-guardian")


class PredictionAnalyticsService:
    """Track prediction performance, confidence trends, and seizure correlations."""

    def __init__(self, db: Session):
        self.db = db

    def get_system_health(self) -> Dict[str, Any]:
        """Get overall system health status."""
        from app.core.mqtt_client import mqtt_client
        from app.services.model_service import model_service

        db_healthy = False
        try:
            self.db.execute(func.count(SensorData.id))
            db_healthy = True
        except Exception:
            db_healthy = False

        return {
            "status": "healthy" if db_healthy else "degraded",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "database": "healthy" if db_healthy else "unhealthy",
                "mqtt": "connected" if mqtt_client._connected else "disconnected",
                "eeg_model": "loaded" if model_service.is_loaded else "not_loaded",
                "sensor_model": "available",
            },
            "model_info": {
                "eeg_loaded": model_service.is_loaded,
                "sensor_version": "sensor-heuristic-v1.0",
            },
        }

    def get_prediction_confidence_trend(self, user_id: int, days: int = 30) -> Dict[str, Any]:
        """Get prediction confidence trend for a patient over time."""
        start_date = datetime.now() - timedelta(days=days)
        alerts = (
            self.db.query(Alert)
            .filter(Alert.user_id == user_id, Alert.alert_type == "seizure_detection", Alert.created_at >= start_date)
            .order_by(Alert.created_at.asc())
            .all()
        )
        confidence_values = [a.confidence for a in alerts if a.confidence is not None]
        daily_confidence = {}
        for a in alerts:
            if a.confidence is not None:
                day = str(a.created_at.date())
                if day not in daily_confidence:
                    daily_confidence[day] = []
                daily_confidence[day].append(a.confidence)

        trend = []
        for day in sorted(daily_confidence.keys()):
            vals = daily_confidence[day]
            trend.append({
                "date": day,
                "avg_confidence": round(sum(vals) / len(vals), 4),
                "count": len(vals),
                "max_confidence": round(max(vals), 4),
            })

        return {
            "user_id": user_id,
            "period_days": days,
            "total_alerts": len(alerts),
            "avg_confidence": round(sum(confidence_values) / len(confidence_values), 4) if confidence_values else 0,
            "trend": trend,
        }

    def get_seizure_correlation(self, user_id: int, days: int = 90) -> Dict[str, Any]:
        """Analyze which vitals correlate most with seizure events."""
        start_date = datetime.now() - timedelta(days=days)
        seizure_alerts = (
            self.db.query(Alert)
            .filter(Alert.user_id == user_id, Alert.alert_type == "seizure_detection", Alert.created_at >= start_date)
            .all()
        )
        seizure_times = [a.created_at for a in seizure_alerts]
        correlations = {}

        for vital_name, vital_col in [("heart_rate", SensorData.heart_rate), ("spo2", SensorData.spo2), ("temperature", SensorData.temperature)]:
            seizure_vals = []
            normal_vals = []
            for st in seizure_times:
                nearby = (
                    self.db.query(SensorData)
                    .filter(SensorData.user_id == user_id, SensorData.created_at.between(st - timedelta(minutes=5), st + timedelta(minutes=5)))
                    .all()
                )
                for s in nearby:
                    val = getattr(s, vital_name, None)
                    if val is not None:
                        seizure_vals.append(val)

            normal_data = (
                self.db.query(SensorData)
                .filter(SensorData.user_id == user_id, SensorData.created_at >= start_date)
                .limit(200)
                .all()
            )
            for s in normal_data:
                val = getattr(s, vital_name, None)
                if val is not None:
                    normal_vals.append(val)

            if seizure_vals and normal_vals:
                avg_seizure = sum(seizure_vals) / len(seizure_vals)
                avg_normal = sum(normal_vals) / len(normal_vals)
                diff_pct = ((avg_seizure - avg_normal) / avg_normal * 100) if avg_normal != 0 else 0
                correlations[vital_name] = {
                    "avg_during_seizure": round(avg_seizure, 2),
                    "avg_normal": round(avg_normal, 2),
                    "difference_pct": round(diff_pct, 1),
                    "sample_seizure": len(seizure_vals),
                    "sample_normal": len(normal_vals),
                }

        return {
            "user_id": user_id,
            "period_days": days,
            "seizure_count": len(seizure_alerts),
            "correlations": correlations,
        }

    def get_model_performance_summary(self, days: int = 30) -> Dict[str, Any]:
        """Get model performance summary across all patients."""
        start_date = datetime.now() - timedelta(days=days)
        total_alerts = self.db.query(func.count(Alert.id)).filter(Alert.alert_type == "seizure_detection", Alert.created_at >= start_date).scalar() or 0
        critical_count = self.db.query(func.count(Alert.id)).filter(Alert.alert_type == "seizure_detection", Alert.severity == "critical", Alert.created_at >= start_date).scalar() or 0
        warning_count = self.db.query(func.count(Alert.id)).filter(Alert.alert_type == "seizure_detection", Alert.severity == "warning", Alert.created_at >= start_date).scalar() or 0
        resolved_count = self.db.query(func.count(Alert.id)).filter(Alert.alert_type == "seizure_detection", Alert.is_resolved == True, Alert.created_at >= start_date).scalar() or 0
        false_positive_rate = 0
        if total_alerts > 0:
            resolved_non_critical = self.db.query(func.count(Alert.id)).filter(Alert.alert_type == "seizure_detection", Alert.severity == "warning", Alert.is_resolved == True, Alert.created_at >= start_date).scalar() or 0
            if resolved_count > 0:
                false_positive_rate = round(resolved_non_critical / resolved_count * 100, 1)

        avg_confidence = self.db.query(func.avg(Alert.confidence)).filter(Alert.alert_type == "seizure_detection", Alert.created_at >= start_date).scalar() or 0

        return {
            "period_days": days,
            "total_seizure_alerts": total_alerts,
            "critical_alerts": critical_count,
            "warning_alerts": warning_count,
            "resolved_alerts": resolved_count,
            "avg_confidence": round(float(avg_confidence), 4) if avg_confidence else 0,
            "estimated_false_positive_rate": false_positive_rate,
            "timestamp": datetime.now().isoformat(),
        }