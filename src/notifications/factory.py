"""
Notification Factory - Factory Design Pattern & Dependency Inversion Principle (SOLID)
Bildirim nesnesi oluşturmaktan sorumlu
"""

from enum import Enum
from typing import Optional
from .base import NotificationBase
from .telegram import TelegramNotification
from .email import EmailNotification


class NotificationType(Enum):
    """Bildirim tipleri"""
    TELEGRAM = "telegram"
    EMAIL = "email"


class NotificationFactory:
    """
    Factory Pattern - Bildirim nesneleri yaratmak için factory
    
    Avantajlar:
    - Istemci kodu, spesifik sınıftan bağımsız hale gelir
    - Yeni bildirim türü eklemek kolay olur
    - Nesne yaratma işi merkezi bir yerde yapılır
    """
    
    _notification_types = {
        NotificationType.TELEGRAM: TelegramNotification,
        NotificationType.EMAIL: EmailNotification,
    }
    
    @staticmethod
    def create(
        notification_type: NotificationType,
        **kwargs
    ) -> NotificationBase:
        """
        Bildirim nesnesi oluştur
        
        Args:
            notification_type: Bildirim tipi (TELEGRAM veya EMAIL)
            **kwargs: Bildirim sınıfına gönderilecek argümanlar
            
        Returns:
            NotificationBase instance
            
        Raises:
            ValueError: Geçersiz bildirim tipi
        """
        if notification_type not in NotificationFactory._notification_types:
            raise ValueError(
                f"Geçersiz bildirim tipi: {notification_type}. "
                f"Desteklenenler: {', '.join([t.value for t in NotificationType])}"
            )
        
        notification_class = NotificationFactory._notification_types[notification_type]
        return notification_class(**kwargs)
    
    @staticmethod
    def register_notification_type(
        notification_type: NotificationType,
        notification_class: type
    ) -> None:
        """
        Yeni bildirim tipi kaydet (Esneklik için)
        
        Args:
            notification_type: Bildirim tipi enum'u
            notification_class: NotificationBase'den türeyen sınıf
        """
        if not issubclass(notification_class, NotificationBase):
            raise TypeError(
                f"{notification_class.__name__} NotificationBase'den türemelidir"
            )
        NotificationFactory._notification_types[notification_type] = notification_class
