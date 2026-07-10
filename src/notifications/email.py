"""
Email Notification - Single Responsibility Principle (SOLID)
Sadece E-posta bildirim gönderme işleminden sorumlu
"""

import re
from typing import Optional
from .base import NotificationBase


class EmailNotification(NotificationBase):
    """E-posta üzerinden bildirim gönderme"""
    
    def __init__(self, smtp_server: Optional[str] = None):
        """
        Args:
            smtp_server: SMTP sunucu adresi (opsiyonel, simülasyon için)
        """
        self.smtp_server = smtp_server or "SMTP_SERVER_SIMULATED"
        self.service_name = "Email"
    
    def send(self, recipient: str, subject: str, message: str) -> bool:
        """
        E-posta ile bildirim gönder (simüle edilmiş)
        
        Args:
            recipient: E-posta adresi
            subject: E-posta konusu
            message: E-posta içeriği
            
        Returns:
            Başarılı mı
        """
        if not self.validate_recipient(recipient):
            return False
        
        # Simüle edilmiş gönderim
        self._log_simulated_send(recipient, subject, message)
        return True
    
    def validate_recipient(self, recipient: str) -> bool:
        """
        E-posta adresini doğrula
        
        Args:
            recipient: E-posta adresi
            
        Returns:
            Geçerli mi
        """
        # Basit e-posta validasyonu
        email_pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return bool(re.match(email_pattern, recipient))
    
    def _log_simulated_send(self, email: str, subject: str, message: str) -> None:
        """Simüle edilmiş e-posta gönderimi log'la"""
        print(f"[{self.service_name}] Kime: {email}")
        print(f"[{self.service_name}] Konu: {subject}")
        print(f"[{self.service_name}] İçerik: {message}")
        print(f"[{self.service_name}] ✅ Gönderildi (Simüle)\n")
