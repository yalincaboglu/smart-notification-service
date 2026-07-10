"""
FastAPI Application Factory
SOLID Principle: Single Responsibility - API setup
"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sys
from pathlib import Path

# Import routes (relative imports)
from .routes import router as notifications_router
from logger import LogManager

# Logger
logger = LogManager.get_logger()


def create_app() -> FastAPI:
    """
    FastAPI application factory
    
    Returns:
        FastAPI application instance
    """
    
    # FastAPI instance oluştur
    app = FastAPI(
        title="Smart Notification API",
        description="Mikroservis Tabanlı Akıllı Bildirim ve Loglama Altyapısı",
        version="0.1.0",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json"
    )
    
    # CORS middleware (gerekirse)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Production'da belirli origins belirtilmeli
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        """Tüm request'leri log'la"""
        logger.info(f"{request.method} {request.url.path}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response
    
    # Routes ekle
    app.include_router(notifications_router)
    
    # Health check endpoint
    @app.get("/health", tags=["Health"])
    async def health_check():
        """API sağlık durumunu kontrol et"""
        return {
            "status": "healthy",
            "version": "0.1.0",
            "message": "Smart Notification API çalışıyor!"
        }
    
    # Root endpoint
    @app.get("/", tags=["Info"])
    async def root():
        """API bilgisi"""
        return {
            "name": "Smart Notification API",
            "version": "0.1.0",
            "description": "Mikroservis Tabanlı Bildirim Sistemi",
            "docs": "/api/docs",
            "api_v1": "/v1"
        }
    
    # Exception handler'lar
    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """ValueError handler"""
        logger.error(f"ValueError: {str(exc)}")
        return JSONResponse(
            status_code=400,
            content={
                "error": "ValueError",
                "detail": str(exc)
            }
        )
    
    # Startup event
    @app.on_event("startup")
    async def startup():
        """Uygulama başlangıçı"""
        logger.info("=" * 60)
        logger.info("Smart Notification API Başlatıldı")
        logger.info("=" * 60)
    
    # Shutdown event
    @app.on_event("shutdown")
    async def shutdown():
        """Uygulama kapanış"""
        logger.info("=" * 60)
        logger.info("Smart Notification API Durduruldu")
        logger.info("=" * 60)
    
    return app


# FastAPI instance
app = create_app()
