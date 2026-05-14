"""Smart Guardian - IoT device API key authentication"""

import logging
from fastapi import Header, HTTPException, status

logger = logging.getLogger("smart-guardian")


class DeviceAuthManager:
    """Manage IoT device API keys. In production, back this with a database."""

    def __init__(self):
        self._devices = {}

    def register_device(self, device_id: str, api_key: str):
        self._devices[device_id] = api_key
        logger.info("Device registered: %s", device_id)

    def validate_device(self, device_id: str, api_key: str) -> bool:
        stored_key = self._devices.get(device_id)
        if not stored_key:
            return False
        return stored_key == api_key

    def is_registered(self, device_id: str) -> bool:
        return device_id in self._devices

    def revoke_device(self, device_id: str):
        if device_id in self._devices:
            del self._devices[device_id]
            logger.info("Device revoked: %s", device_id)


device_auth = DeviceAuthManager()


async def verify_device_api_key(
    x_device_id: str = Header(None),
    x_api_key: str = Header(None),
):
    """FastAPI dependency to verify IoT device API key via headers."""
    if not x_device_id or not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Device auth required. Provide X-Device-Id and X-Api-Key headers.",
        )
    if not device_auth.validate_device(x_device_id, x_api_key):
        logger.warning("Invalid device auth attempt: device=%s", x_device_id)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid device credentials.",
        )
    return x_device_id