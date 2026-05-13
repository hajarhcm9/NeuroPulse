"""Smart Guardian - Sensor data service"""

import logging
from typing import List
from fastapi import HTTPException, status
from app.models.sensor_data import SensorData
from app.repositories.sensor_repository import SensorRepository
from app.schemas.sensor_data import SensorDataCreate, SensorDataResponse

logger = logging.getLogger("smart-guardian")


class SensorService:
    """Business logic for sensor data"""

    def __init__(self, db):
        self.sensor_repo = SensorRepository(db)

    def store_sensor_data(self, data: SensorDataCreate) -> SensorDataResponse:
        sensor = SensorData(
            user_id=data.user_id,
            device_id=data.device_id,
            sensor_type=data.sensor_type,
            heart_rate=data.heart_rate,
            spo2=data.spo2,
            temperature=data.temperature,
            accelerometer_x=data.accelerometer_x,
            accelerometer_y=data.accelerometer_y,
            accelerometer_z=data.accelerometer_z,
            gyroscope_x=data.gyroscope_x,
            gyroscope_y=data.gyroscope_y,
            gyroscope_z=data.gyroscope_z,
            emg_signal=data.emg_signal,
            eda_signal=data.eda_signal,
            raw_data=data.raw_data,
        )
        sensor = self.sensor_repo.create(sensor)
        logger.info("Sensor data stored: device=%s user=%s", data.device_id, data.user_id)
        return SensorDataResponse.model_validate(sensor)

    def get_user_data(self, user_id: int, limit: int = 100) -> List[SensorDataResponse]:
        data = self.sensor_repo.get_by_user(user_id, limit)
        return [SensorDataResponse.model_validate(d) for d in data]

    def get_device_data(self, device_id: str, limit: int = 100) -> List[SensorDataResponse]:
        data = self.sensor_repo.get_by_device(device_id, limit)
        return [SensorDataResponse.model_validate(d) for d in data]

    def get_latest(self, user_id: int) -> SensorDataResponse:
        data = self.sensor_repo.get_latest_by_user(user_id)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No sensor data found")
        return SensorDataResponse.model_validate(data)

    def process_mqtt_message(self, topic: str, payload: dict):
        """Process incoming MQTT sensor data"""
        try:
            sensor_data = SensorDataCreate(**payload)
            self.store_sensor_data(sensor_data)
            logger.info("MQTT data processed for device: %s", payload.get("device_id"))
        except Exception as e:
            logger.error("Error processing MQTT data: %s", e)
