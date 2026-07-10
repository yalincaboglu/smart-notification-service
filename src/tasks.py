"""
Celery tasks for background notification processing
"""

from celery_config import celery_app
from notifications import NotificationFactory, NotificationType
from logger import LogManager

logger = LogManager.get_logger()


@celery_app.task(name="tasks.send_notification_task", bind=True)
def send_notification_task(
    self,
    notification_type: str,
    recipient: str,
    subject: str,
    message: str,
) -> dict:
    """Bildirim gönderimini arka planda işle"""
    logger.info(
        f"Task {self.request.id}: Sending {notification_type} notification "
        f"to {recipient}"
    )

    try:
        notifier = NotificationFactory.create(NotificationType(notification_type))

        if not notifier.validate_recipient(recipient):
            logger.warning(
                f"Task {self.request.id}: Invalid recipient {recipient} "
                f"for {notification_type}"
            )
            return {
                "success": False,
                "message": "Invalid recipient format",
                "notification_type": notification_type,
                "recipient": recipient,
            }

        result = notifier.send(
            recipient=recipient,
            subject=subject,
            message=message,
        )

        if not result:
            logger.error(
                f"Task {self.request.id}: Failed to send {notification_type} notification"
            )
            return {
                "success": False,
                "message": "Notification could not be sent",
                "notification_type": notification_type,
                "recipient": recipient,
            }

        logger.info(
            f"Task {self.request.id}: {notification_type} notification sent successfully"
        )
        return {
            "success": True,
            "message": "Notification queued and sent asynchronously",
            "notification_type": notification_type,
            "recipient": recipient,
        }

    except Exception as exc:
        logger.error(f"Task {self.request.id}: Exception: {str(exc)}")
        raise self.retry(exc=exc, countdown=10, max_retries=3)
