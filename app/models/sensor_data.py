"""Smart Guardian - Sensor data model"""

from sqlalchemy import Column, String, Float, Integer, ForeignKey, Text
from app.models.base import BaseModel


class SensorData(BaseModel):
    """Sensor readings from IoT bracelet"""
    __tablename__ = "sensor_data"

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    device_id = Column(String(100), nullable=False, index=True)
    sensor_type = Column(String(50), nullable=False)
    heart_rate = Column(Float, nullable=True)
    spo2 = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    accelerometer_x = Column(Float, nullable=True)
    accelerometer_y = Column(Float, nullable=True)
    accelerometer_z = Column(Float, nullable=True)
    gyroscope_x = Column(Float, nullable=True)
    gyroscope_y = Column(Float, nullable=True)
    gyroscope_z = Column(Float, nullable=True)
    emg_signal = Column(Float, nullable=True)
    eda_signal = Column(Float, nullable=True)
    raw_data = Column(Text, nullable=True)
