"""Smart Guardian - Audit logging for medical compliance (PHI access tracking)"""

import logging
from typing import Optional

audit_logger = logging.getLogger("smart-guardian.audit")


class AuditLogger:
    """Audit logging for Protected Health Information access compliance."""

    @staticmethod
    def log_access(
        user_id: Optional[int],
        action: str,
        resource: str,
        resource_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        details: Optional[dict] = None,
    ):
        audit_logger.info(
            "AUDIT | user=%s | action=%s | resource=%s | id=%s | ip=%s | details=%s",
            user_id, action, resource, resource_id, ip_address, details or {},
        )

    @staticmethod
    def log_data_access(user_id: int, data_type: str, record_id: int, ip: str = None):
        audit_logger.info(
            "AUDIT_DATA_ACCESS | user=%s | type=%s | record=%s | ip=%s",
            user_id, data_type, record_id, ip,
        )

    @staticmethod
    def log_alert_event(user_id: int, alert_type: str, severity: str, details: dict = None):
        audit_logger.info(
            "AUDIT_ALERT | user=%s | type=%s | severity=%s | details=%s",
            user_id, alert_type, severity, details or {},
        )

    @staticmethod
    def log_auth_event(username: str, event: str, success: bool, ip: str = None):
        audit_logger.info(
            "AUDIT_AUTH | user=%s | event=%s | success=%s | ip=%s",
            username, event, success, ip,
        )

    @staticmethod
    def log_device_event(device_id: str, event: str, details: dict = None):
        audit_logger.info(
            "AUDIT_DEVICE | device=%s | event=%s | details=%s",
            device_id, event, details or {},
        )


audit = AuditLogger()