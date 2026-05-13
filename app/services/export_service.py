"""Smart Guardian - Export Service (CSV/JSON Reports)"""

import logging
import csv
import io
import json
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.alert import Alert
from app.models.sensor_data import SensorData

logger = logging.getLogger("smart-guardian")


class ExportService:
    """Service for exporting data as CSV or JSON reports"""

    def __init__(self, db: Session):
        self.db = db

    def _get_alerts_data(self, user_id: int, days: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fetch alerts data for export"""
        query = self.db.query(Alert).filter(Alert.user_id == user_id)
        if days:
            start_date = datetime.now() - timedelta(days=days)
            query = query.filter(Alert.created_at >= start_date)
        alerts = query.order_by(Alert.created_at.desc()).all()
        return [{
            "id": a.id,
            "device_id": a.device_id,
            "alert_type": a.alert_type,
            "severity": a.severity,
            "confidence": a.confidence,
            "heart_rate": a.heart_rate,
            "spo2": a.spo2,
            "message": a.message,
            "is_read": a.is_read,
            "is_resolved": a.is_resolved,
            "created_at": a.created_at.isoformat(),
        } for a in alerts]

    def _get_sensor_data(self, user_id: int, days: Optional[int] = None) -> List[Dict[str, Any]]:
        """Fetch sensor data for export"""
        query = self.db.query(SensorData).filter(SensorData.user_id == user_id)
        if days:
            start_date = datetime.now() - timedelta(days=days)
            query = query.filter(SensorData.created_at >= start_date)
        sensors = query.order_by(SensorData.created_at.desc()).limit(1000).all()
        return [{
            "id": s.id,
            "device_id": s.device_id,
            "sensor_type": s.sensor_type,
            "heart_rate": s.heart_rate,
            "spo2": s.spo2,
            "temperature": s.temperature,
            "accelerometer_x": s.accelerometer_x,
            "accelerometer_y": s.accelerometer_y,
            "accelerometer_z": s.accelerometer_z,
            "gyroscope_x": s.gyroscope_x,
            "gyroscope_y": s.gyroscope_y,
            "gyroscope_z": s.gyroscope_z,
            "emg_signal": s.emg_signal,
            "eda_signal": s.eda_signal,
            "created_at": s.created_at.isoformat(),
        } for s in sensors]

    def export_alerts_csv(self, user_id: int, days: Optional[int] = None) -> str:
        """Export alerts as CSV string"""
        data = self._get_alerts_data(user_id, days)
        if not data:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

    def export_alerts_json(self, user_id: int, days: Optional[int] = None) -> str:
        """Export alerts as JSON string"""
        data = self._get_alerts_data(user_id, days)
        return json.dumps(data, indent=2, default=str)

    def export_sensor_csv(self, user_id: int, days: Optional[int] = None) -> str:
        """Export sensor data as CSV string"""
        data = self._get_sensor_data(user_id, days)
        if not data:
            return ""
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        return output.getvalue()

    def export_sensor_json(self, user_id: int, days: Optional[int] = None) -> str:
        """Export sensor data as JSON string"""
        data = self._get_sensor_data(user_id, days)
        return json.dumps(data, indent=2, default=str)

    def export_full_report_json(self, user_id: int, days: Optional[int] = None) -> str:
        """Export a full report with alerts and sensor data as JSON"""
        report = {
            "export_date": datetime.now().isoformat(),
            "user_id": user_id,
            "period_days": days,
            "alerts": self._get_alerts_data(user_id, days),
            "sensor_data": self._get_sensor_data(user_id, days),
            "summary": {
                "total_alerts": len(self._get_alerts_data(user_id, days)),
                "critical_alerts": len([a for a in self._get_alerts_data(user_id, days) if a['severity'] == "critical"]),
                "total_sensor_readings": len(self._get_sensor_data(user_id, days)),
            },
        }
        return json.dumps(report, indent=2, default=str)
