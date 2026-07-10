"""
API Routes - Notification endpoints
SOLID Principle: Single Responsibility - HTTP request handling only
"""

from fastapi import APIRouter, Depends, HTTPException, status
from ..models import (
    SendNotificationRequest,
    SendNotificationResponse,
    ErrorResponse,
    NotificationTypeEnum
)
from ..dependencies import get_notification_service, get_logger
from ..tasks import send_notification_task
from notifications import NotificationBase
import logging

# Router oluştur
router = APIRouter(
    prefix="/v1/notifications",
    tags=["Notifications"],
    responses={
        404: {"description": "Not found"},
        422: {"description": "Validation error"}
    }
)


@router.post(
    "/send",
    response_model=SendNotificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Bildirim gönder",
    description="Telegram veya Email aracılığıyla bildirim gönder"
)
async def send_notification(
    request: SendNotificationRequest,
    logger: logging.Logger = Depends(get_logger)
) -> SendNotificationResponse:
    """
    Bildirim gönder
    
    - **notification_type**: telegram veya email
    - **recipient**: Chat ID (telegram) veya email adresi
    - **subject**: Bildirim başlığı
    - **message**: Bildirim mesajı
    """
    
    try:
        logger.info(
            f"Sending {request.notification_type.value} notification "
            f"to {request.recipient}"
        )
        
        # Dependency injection ile notifier oluştur
        notifier: NotificationBase = get_notification_service(
            request.notification_type.value
        )
        
        # Alıcıyı doğrula
        if not notifier.validate_recipient(request.recipient):
            logger.warning(
                f"Invalid recipient for {request.notification_type.value}: "
                f"{request.recipient}"
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Geçersiz {request.notification_type.value} formatı: {request.recipient}"
            )
        
        # Bildirimi kuyruğa ekle
        task = send_notification_task.delay(
            request.notification_type.value,
            request.recipient,
            request.subject,
            request.message,
        )
        
        logger.info(
            f"Task queued: {task.id} for {request.notification_type.value} notification"
        )
        
        return SendNotificationResponse(
            success=True,
            message=f"{request.notification_type.value.title()} bildirimi kuyruğa eklendi.",
            notification_type=request.notification_type,
            recipient=request.recipient,
            task_id=task.id,
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error in send_notification: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Beklenmeyen bir hata oluştu"
        )


@router.get(
    "/types",
    summary="Desteklenen bildirim tiplerini listele",
    description="Sistemde desteklenen tüm bildirim tiplerini döndür"
)
async def get_notification_types(logger: logging.Logger = Depends(get_logger)):
    """Desteklenen bildirim tiplerini listele"""
    
    types = [
        {
            "type": "telegram",
            "description": "Telegram Bot API üzerinden bildirim",
            "recipient_format": "Chat ID (numerik)"
        },
        {
            "type": "email",
            "description": "SMTP üzerinden email bildirimi",
            "recipient_format": "Email adresi"
        }
    ]
    
    logger.debug("Notification types requested")
    return {"notification_types": types}


@router.post(
    "/validate",
    summary="Alıcı formatını doğrula",
    description="Verilen alıcının format açısından geçerli olup olmadığını kontrol et"
)
async def validate_recipient(
    notification_type: NotificationTypeEnum,
    recipient: str,
    logger: logging.Logger = Depends(get_logger)
):
    """Alıcı formatını doğrula"""
    
    try:
        notifier = get_notification_service(notification_type.value)
        is_valid = notifier.validate_recipient(recipient)
        
        logger.debug(
            f"Validation for {notification_type.value}: {recipient} = {is_valid}"
        )
        
        return {
            "notification_type": notification_type,
            "recipient": recipient,
            "is_valid": is_valid,
            "message": "Hazır" if is_valid else "Geçersiz format"
        }
    
    except Exception as e:
        logger.error(f"Validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Doğrulama sırasında hata oluştu"
        )
