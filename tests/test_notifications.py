"""
Test - Notification Factory ve bildirim sınıfları için testler
"""

import pytest
import sys
from pathlib import Path

# src dizinini Python path'e ekle
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from notifications import (
    NotificationFactory,
    NotificationType,
    TelegramNotification,
    EmailNotification,
)


class TestTelegramNotification:
    """Telegram bildirim testleri"""
    
    def test_valid_chat_id(self):
        """Geçerli Chat ID doğrulama"""
        telegram = TelegramNotification()
        assert telegram.validate_recipient("123456789") is True
    
    def test_invalid_chat_id(self):
        """Geçersiz Chat ID doğrulama"""
        telegram = TelegramNotification()
        assert telegram.validate_recipient("invalid-id") is False
        assert telegram.validate_recipient("abc123") is False
    
    def test_send_valid_message(self):
        """Geçerli mesaj gönderme"""
        telegram = TelegramNotification()
        result = telegram.send(
            recipient="123456789",
            subject="Test",
            message="Test Mesajı"
        )
        assert result is True
    
    def test_send_invalid_recipient(self):
        """Geçersiz alıcıya mesaj gönderme"""
        telegram = TelegramNotification()
        result = telegram.send(
            recipient="invalid",
            subject="Test",
            message="Test Mesajı"
        )
        assert result is False


class TestEmailNotification:
    """Email bildirim testleri"""
    
    def test_valid_email(self):
        """Geçerli email doğrulama"""
        email = EmailNotification()
        assert email.validate_recipient("user@example.com") is True
    
    def test_invalid_email(self):
        """Geçersiz email doğrulama"""
        email = EmailNotification()
        assert email.validate_recipient("invalid-email") is False
        assert email.validate_recipient("user@") is False
        assert email.validate_recipient("@example.com") is False
    
    def test_send_valid_message(self):
        """Geçerli mesaj gönderme"""
        email = EmailNotification()
        result = email.send(
            recipient="user@example.com",
            subject="Test Konusu",
            message="Test Mesajı"
        )
        assert result is True
    
    def test_send_invalid_recipient(self):
        """Geçersiz alıcıya mesaj gönderme"""
        email = EmailNotification()
        result = email.send(
            recipient="invalid-email",
            subject="Test Konusu",
            message="Test Mesajı"
        )
        assert result is False


class TestNotificationFactory:
    """Factory Pattern testleri"""
    
    def test_create_telegram_notification(self):
        """Telegram notifier oluştur"""
        notifier = NotificationFactory.create(NotificationType.TELEGRAM)
        assert isinstance(notifier, TelegramNotification)
    
    def test_create_email_notification(self):
        """Email notifier oluştur"""
        notifier = NotificationFactory.create(NotificationType.EMAIL)
        assert isinstance(notifier, EmailNotification)
    
    def test_create_invalid_notification_type(self):
        """Geçersiz bildirim tipi ile hata"""
        with pytest.raises(ValueError):
            NotificationFactory.create("invalid_type")  # type: ignore
    
    def test_factory_with_custom_token(self):
        """Custom token ile factory"""
        custom_token = "CUSTOM_TOKEN_123"
        notifier = NotificationFactory.create(
            NotificationType.TELEGRAM,
            bot_token=custom_token
        )
        assert isinstance(notifier, TelegramNotification)
        assert notifier.bot_token == custom_token
