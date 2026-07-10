"""
Smart Notification Application - Multiple Modes
CLI mode: Demo ve test amaçlı
API mode: FastAPI server (production ready)
"""

import sys
from pathlib import Path
from notifications import NotificationFactory, NotificationType
from logger import LogManager


def cli_demo():
    """CLI Demo modunda çalıştır (orijinal demo)"""
    
    # Logger'ı başlat
    LogManager.initialize()
    logger = LogManager.get_logger()
    
    logger.info("=" * 60)
    logger.info("Smart Notification Sistemi Başlatıldı (CLI Mode)")
    logger.info("=" * 60)
    
    # ============ TELEGRAM ÖRNEK ============
    logger.info("\n📱 TELEGRAM BİLDİRİMİ GÖNDERİLİYOR...")
    
    try:
        telegram_notifier = NotificationFactory.create(
            NotificationType.TELEGRAM
        )
        
        result = telegram_notifier.send(
            recipient="123456789",
            subject="Sistem Güncellemesi",
            message="Sistem başarıyla güncellenmiştir. Yeni özellikler eklenmiştir."
        )
        
        if result:
            logger.info("✅ Telegram bildirimi başarıyla gönderildi")
        else:
            logger.error("❌ Telegram bildirimi gönderilemedi")
    
    except Exception as e:
        logger.error(f"Telegram bildirimi hatası: {str(e)}")
    
    # ============ EMAIL ÖRNEK ============
    logger.info("\n📧 EMAIL BİLDİRİMİ GÖNDERİLİYOR...")
    
    try:
        email_notifier = NotificationFactory.create(
            NotificationType.EMAIL
        )
        
        result = email_notifier.send(
            recipient="user@example.com",
            subject="Hoşgeldiniz!",
            message="Akıllı Bildirim Sistemine hoşgeldiniz. Sistemi kullanmaya başlayabilirsiniz."
        )
        
        if result:
            logger.info("✅ Email bildirimi başarıyla gönderildi")
        else:
            logger.error("❌ Email bildirimi gönderilemedi")
    
    except Exception as e:
        logger.error(f"Email bildirimi hatası: {str(e)}")
    
    # ============ HATA YÖNETME ÖRNEK ============
    logger.info("\n⚠️ HATA YÖNETME ÖRNEĞİ...")
    
    try:
        telegram_notifier = NotificationFactory.create(
            NotificationType.TELEGRAM
        )
        result = telegram_notifier.send(
            recipient="invalid-chat-id",
            subject="Test",
            message="Bu çalışmayacak"
        )
        
        if not result:
            logger.warning("⚠️ Geçersiz Telegram Chat ID yapısı")
    
    except Exception as e:
        logger.error(f"Hata: {str(e)}")
    
    logger.info("\n" + "=" * 60)
    logger.info("CLI Demo Tamamlandı!")
    logger.info("=" * 60)


def api_mode():
    """API modunda FastAPI server'ı çalıştır"""
    
    LogManager.initialize()
    logger = LogManager.get_logger()
    
    logger.info("=" * 60)
    logger.info("Smart Notification API Server Başlatılıyor...")
    logger.info("=" * 60)
    
    try:
        # FastAPI app'ı import et ve çalıştır
        import uvicorn
        from api import app
        
        logger.info("🚀 API sunucusu başladı")
        logger.info("📚 Swagger UI: http://localhost:8000/api/docs")
        logger.info("📋 ReDoc: http://localhost:8000/api/redoc")
        
        # Uvicorn server'ı çalıştır
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
    
    except ImportError as e:
        logger.error(f"FastAPI bağımlılıkları yüklenmemiş: {str(e)}")
        logger.error("Lütfen şunu çalıştırın: pip install fastapi uvicorn")
        sys.exit(1)
    except Exception as e:
        logger.error(f"API server hatası: {str(e)}")
        sys.exit(1)


def main():
    """Ana entry point"""
    
    # Komut satırı argümanı kontrol et
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "api":
            api_mode()
        elif mode == "cli":
            cli_demo()
        elif mode in ["-h", "--help", "help"]:
            print("""
Smart Notification - Usage:
    
    python src/main.py              # Default: CLI mode (demo)
    python src/main.py cli          # CLI mode (demo)
    python src/main.py api          # API mode (FastAPI server)
    
FastAPI server çalışırken:
    📚 Swagger UI: http://localhost:8000/api/docs
    📋 ReDoc: http://localhost:8000/api/redoc
    🔗 Health: http://localhost:8000/health
            """)
        else:
            print(f"Bilinmeyen mod: {mode}")
            print("Kullanım: python src/main.py [cli|api]")
            sys.exit(1)
    else:
        # Default: CLI mode
        cli_demo()


if __name__ == "__main__":
    main()

