"""
Base notification interface - Interface Segregation Principle (SOLID)
Tüm bildirim türleri için abstract base class
"""

from abc import ABC, abstractmethod
from typing import Optional


class NotificationBase(ABC):
    """
    Abstract base class - tüm bildirim türlerinin implement etmesi gereken interface
    """
    
    @abstractmethod
    def send(self, recipient: str, subject: str, message: str) -> bool:
        """
        Bildirim göndermek için abstract method
        
        Args:
            recipient: Alıcı (email, chat_id, v.b.)
            subject: Konu/Başlık
            message: Mesaj içeriği
            
        Returns:
            Başarılı mı (True/False)
        """
        pass
    
    @abstractmethod
    def validate_recipient(self, recipient: str) -> bool:
        """
        Alıcı formatını doğrula
        
        Args:
            recipient: Doğrulanacak alıcı
            
        Returns:
            Geçerli mi (True/False)
        """
        pass
