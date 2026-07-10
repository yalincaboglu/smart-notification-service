"""
Telegram Notification - Single Responsibility Principle (SOLID)
Sadece Telegram bildirim gönderme işleminden sorumlu
"""

import re
from typing import Optional
from .base import NotificationBase


class TelegramNotification(NotificationBase):
    """Telegram üzerinden bildirim gönderme"""
    
    def __init__(self, bot_token: Optional[str] = None):
        """
        Args:
            bot_token: Telegram bot tokeni (opsiyonel, simülasyon için)
        """
        self.bot_token = bot_token or "TELEGRAM_BOT_TOKEN_SIMULATED"
        self.service_name = "Telegram"
    
    def send(self, recipient: str, subject: str, message: str) -> bool:
        """
        Telegram'a bildirim gönder (simüle edilmiş)
        
        Args:
            recipient: Chat ID
            subject: Bildirim başlığı
            message: Bildirim mesajı
            
        Returns:
            Başarılı mı
        """
        if not self.validate_recipient(recipient):
            return False
        
        # Simüle edilmiş gönderim
        full_message = f"📢 {subject}\n\n{message}"
        self._log_simulated_send(recipient, full_message)
        return True
    
    def validate_recipient(self, recipient: str) -> bool:
        """
        Telegram Chat ID'sini doğrula (numara olmalı)
        
        Args:
            recipient: Chat ID
            
        Returns:
            Geçerli mi
        """
        # Chat ID sadece rakam olmalı
        return bool(re.match(r"^\d+$", recipient))
    
    def _log_simulated_send(self, chat_id: str, message: str) -> None:
        """Simüle edilmiş gönderimi log'la"""
        print(f"[{self.service_name}] Chat ID: {chat_id}")
        print(f"[{self.service_name}] Mesaj: {message}")
        print(f"[{self.service_name}] ✅ Gönderildi (Simüle)\n")
