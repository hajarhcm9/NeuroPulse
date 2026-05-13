"""Smart Guardian - Sensor data repository"""

from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.sensor_data import SensorData


class SensorRepository:
    """Data access layer for SensorData model"""

    def __init__(self, db: Session):
        self.db = db

    def create(self, data: SensorData) -> SensorData:
        self.db.add(data)
        self.db.commit()
        self.db.refresh(data)
        return data

    def get_by_id(self, data_id: int) -> Optional[SensorData]:
        return self.db.query(SensorData).filter(SensorData.id == data_id).first()

    def get_by_user(self, user_id: int, limit: int = 100) -> List[SensorData]:
        return self.db.query(SensorData).filter(SensorData.user_id == user_id).order_by(SensorData.created_at.desc()).limit(limit).all()

    def get_by_device(self, device_id: str, limit: int = 100) -> List[SensorData]:
        return self.db.query(SensorData).filter(SensorData.device_id == device_id).order_by(SensorData.created_at.desc()).limit(limit).all()

    def get_latest_by_user(self, user_id: int) -> Optional[SensorData]:
        return self.db.query(SensorData).filter(SensorData.user_id == user_id).order_by(SensorData.created_at.desc()).first()
