"""Sensor-based heuristic seizure detection model."""

from typing import Dict, List
import time

class SensorModel:
    HR_ELEVATED = 110
    HR_CRITICAL = 140
    SPO2_LOW = 93
    SPO2_CRITICAL = 88
    ACCEL_ELEVATED = 2.0
    ACCEL_CRITICAL = 4.0
    EMG_ELEVATED = 0.7
    EMG_CRITICAL = 0.9
    EDA_ELEVATED = 0.6
    EDA_CRITICAL = 0.8
    TEMP_ELEVATED = 38.0
    TEMP_CRITICAL = 39.0
    WEIGHTS = {
        "heart_rate": 0.25,
        "spo2": 0.20,
        "accelerometer": 0.20,
        "emg_signal": 0.15,
        "eda_signal": 0.10,
        "temperature": 0.10,
    }

    def __init__(self):
        self.model_version = "sensor-heuristic-v1.0"

    def predict(self, features: Dict[str, float]) -> Dict:
        risk_score = 0.0
        risk_factors = []

        hr = features.get("heart_rate", 75.0)
        if hr >= self.HR_CRITICAL:
            risk_score += self.WEIGHTS["heart_rate"]
            risk_factors.append("Critical tachycardia: " + str(int(hr)) + " bpm")
        elif hr >= self.HR_ELEVATED:
            risk_score += self.WEIGHTS["heart_rate"] * 0.6
            risk_factors.append("Elevated heart rate: " + str(int(hr)) + " bpm")

        spo2 = features.get("spo2", 98.0)
        if spo2 <= self.SPO2_CRITICAL:
            risk_score += self.WEIGHTS["spo2"]
            risk_factors.append("Critical hypoxia: SpO2 " + str(int(spo2)) + "%")
        elif spo2 <= self.SPO2_LOW:
            risk_score += self.WEIGHTS["spo2"] * 0.6
            risk_factors.append("Low SpO2: " + str(int(spo2)) + "%")

        accel = features.get("accelerometer", 0.5)
        if accel >= self.ACCEL_CRITICAL:
            risk_score += self.WEIGHTS["accelerometer"]
            risk_factors.append("Critical movement: " + str(round(accel, 2)) + "g")
        elif accel >= self.ACCEL_ELEVATED:
            risk_score += self.WEIGHTS["accelerometer"] * 0.6
            risk_factors.append("Elevated movement: " + str(round(accel, 2)) + "g")

        emg = features.get("emg_signal", 0.3)
        if emg >= self.EMG_CRITICAL:
            risk_score += self.WEIGHTS["emg_signal"]
            risk_factors.append("Critical muscle activity: " + str(round(emg, 2)))
        elif emg >= self.EMG_ELEVATED:
            risk_score += self.WEIGHTS["emg_signal"] * 0.6
            risk_factors.append("Elevated muscle activity: " + str(round(emg, 2)))

        eda = features.get("eda_signal", 0.3)
        if eda >= self.EDA_CRITICAL:
            risk_score += self.WEIGHTS["eda_signal"]
            risk_factors.append("Critical skin conductance: " + str(round(eda, 2)))
        elif eda >= self.EDA_ELEVATED:
            risk_score += self.WEIGHTS["eda_signal"] * 0.6
            risk_factors.append("Elevated skin conductance: " + str(round(eda, 2)))

        temp = features.get("temperature", 36.5)
        if temp >= self.TEMP_CRITICAL:
            risk_score += self.WEIGHTS["temperature"]
            risk_factors.append("Critical hyperthermia: " + str(round(temp, 1)) + "C")
        elif temp >= self.TEMP_ELEVATED:
            risk_score += self.WEIGHTS["temperature"] * 0.6
            risk_factors.append("Elevated temperature: " + str(round(temp, 1)) + "C")

        seizure_probability = min(max(risk_score, 0.0), 1.0)
        is_seizure = seizure_probability >= 0.5
        confidence = seizure_probability if is_seizure else 1.0 - seizure_probability

        return {
            "seizure_probability": round(seizure_probability, 4),
            "is_seizure": is_seizure,
            "confidence": round(confidence, 4),
            "model_version": self.model_version,
            "risk_factors": risk_factors,
        }

sensor_model = SensorModel()
