"""Smart Guardian - Notification Service"""

import logging
from datetime import datetime
from typing import List, Optional
from fastapi import HTTPException, status
from app.models.notification import Notification
from app.repositories.notification_repository import NotificationRepository
from app.schemas.notification import NotificationCreate, NotificationResponse, NotificationUpdate

logger = logging.getLogger("smart-guardian")


class NotificationService:
    """Business logic for notifications with email/push stubs"""

    def __init__(self, db):
        self.notification_repo = NotificationRepository(db)

    def create_notification(self, data: NotificationCreate) -> NotificationResponse:
        notification = Notification(
            user_id=data.user_id,
            alert_id=data.alert_id,
            channel=data.channel,
            title=data.title,
            body=data.body,
        )
        notification = self.notification_repo.create(notification)

        send_success = self._dispatch(notification)
        if send_success:
            notification.is_sent = True
            notification.sent_at = datetime.now().isoformat()
            self.notification_repo.update(notification)
            logger.info("Notification sent: id=%d channel=%s user=%d", notification.id, data.channel, data.user_id)
        else:
            notification.error_message = "Failed to send via " + data.channel
            self.notification_repo.update(notification)
            logger.warning("Notification send failed: id=%d channel=%s", notification.id, data.channel)

        return NotificationResponse.model_validate(notification)

    def _dispatch(self, notification: Notification) -> bool:
        """Dispatch notification through the appropriate channel"""
        channel = notification.channel
        if channel == "in_app":
            return True
        elif channel == "email":
            return self._send_email(notification)
        elif channel == "sms":
            return self._send_sms(notification)
        elif channel == "push":
            return self._send_push(notification)
        else:
            logger.error("Unknown notification channel: %s", channel)
            return False

    def _send_email(self, notification: Notification) -> bool:
        """Send email notification (stub - integrate with SendGrid/SMTP later)"""
        logger.info("Email notification stub: to_user=%d subject=%s", notification.user_id, notification.title)
        return True

    def _send_sms(self, notification: Notification) -> bool:
        """Send SMS notification (stub - integrate with Twilio later)"""
        logger.info("SMS notification stub: to_user=%d body=%s", notification.user_id, notification.title)
        return True

    def _send_push(self, notification: Notification) -> bool:
        """Send push notification (stub - integrate with FCM later)"""
        logger.info("Push notification stub: to_user=%d title=%s", notification.user_id, notification.title)
        return True

    def get_user_notifications(self, user_id: int, limit: int = 50) -> List[NotificationResponse]:
        notifications = self.notification_repo.get_by_user(user_id, limit)
        return [NotificationResponse.model_validate(n) for n in notifications]

    def get_unread(self, user_id: int) -> List[NotificationResponse]:
        notifications = self.notification_repo.get_unread_by_user(user_id)
        return [NotificationResponse.model_validate(n) for n in notifications]

    def get_unread_count(self, user_id: int) -> int:
        return self.notification_repo.count_unread(user_id)

    def mark_read(self, notification_id: int) -> NotificationResponse:
        notification = self.notification_repo.get_by_id(notification_id)
        if not notification:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")
        notification.is_read = True
        notification = self.notification_repo.update(notification)
        return NotificationResponse.model_validate(notification)

    def mark_all_read(self, user_id: int) -> dict:
        count = self.notification_repo.mark_all_read(user_id)
        return {"marked_read": count}
