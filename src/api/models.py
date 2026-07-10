"""
Pydantic Data Models - Request/Response validation
SOLID Principle: Data models are separate from business logic
"""

from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, Literal
from enum import Enum


class NotificationTypeEnum(str, Enum):
    """Bildirim tipi enum'u"""
    TELEGRAM = "telegram"
    EMAIL = "email"


class SendNotificationRequest(BaseModel):
    """Bildirim gönderme isteği"""
    
    notification_type: NotificationTypeEnum = Field(
        ...,
        description="Bildirim tipi (telegram veya email)"
    )
    recipient: str = Field(
        ...,
        min_length=1,
        description="Alıcı (Chat ID vya email adresi)"
    )
    subject: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Bildirim başlığı"
    )
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="Bildirim mesajı"
    )
    
    class Config:
        """Pydantic config"""
        json_schema_extra = {
            "example": {
                "notification_type": "email",
                "recipient": "user@example.com",
                "subject": "Test Bildirimi",
                "message": "Bu bir test mesajıdır."
            }
        }


class SendNotificationResponse(BaseModel):
    """Bildirim gönderme yanıtı"""
    
    success: bool = Field(
        ...,
        description="Başarılı mı?"
    )
    message: str = Field(
        ...,
        description="Yanıt mesajı"
    )
    notification_type: NotificationTypeEnum = Field(
        ...,
        description="Gönderilen bildirim tipi"
    )
    recipient: str = Field(
        ...,
        description="Alıcı"
    )
    task_id: Optional[str] = Field(
        None,
        description="Celery task id (arka planda işlenen görev)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Bildirim başarıyla gönderildi",
                "notification_type": "email",
                "recipient": "user@example.com"
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check yanıtı"""
    
    status: str = Field(
        ...,
        description="Sistem durumu (healthy, unhealthy)"
    )
    version: str = Field(
        ...,
        description="API versiyonu"
    )
    message: str = Field(
        ...,
        description="Durum mesajı"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "0.1.0",
                "message": "Smart Notification API çalışıyor!"
            }
        }


class ErrorResponse(BaseModel):
    """Hata yanıtı"""
    
    error: str = Field(
        ...,
        description="Hata tipi"
    )
    detail: str = Field(
        ...,
        description="Hata detayı"
    )
    status_code: int = Field(
        ...,
        description="HTTP status kodu"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "detail": "Geçersiz email formatı",
                "status_code": 422
            }
        }
