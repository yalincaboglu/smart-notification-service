"""
Dependency Injection - Factory pattern ile servis oluşturma
SOLID Principles: Dependency Inversion, Single Responsibility
"""

from fastapi import Depends
from notifications import NotificationFactory, NotificationType, NotificationBase
from logger import LogManager


# Logger singleton
logger = LogManager.get_logger()


def get_notification_service(
    notification_type: str = "email"
) -> NotificationBase:
    """
    Dependency: Notification servisini oluştur (Factory Pattern kullanarak)
    
    Args:
        notification_type: Bildirim tipi (telegram, email)
    
    Returns:
        NotificationBase instance
    """
    try:
        # String'i enum'a dönüştür
        notif_type = NotificationType(notification_type)
        
        # Factory'den notifier oluştur
        notifier = NotificationFactory.create(notif_type)
        
        logger.debug(f"Notification service created: {notif_type.value}")
        return notifier
    
    except ValueError as e:
        logger.error(f"Invalid notification type: {notification_type}")
        raise e


def get_logger():
    """Dependency: Logger'ı enjekte et"""
    return LogManager.get_logger()
