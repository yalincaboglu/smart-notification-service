"""
Logger Manager - Merkezi loglama sistemi
"""

import logging
from datetime import datetime
from pathlib import Path
from typing import Optional


class LogManager:
    """
    Uygulama genelinde loglama işlemlerini yönet
    """
    
    _logger: Optional[logging.Logger] = None
    _log_dir: Optional[Path] = None
    
    @classmethod
    def initialize(cls, log_dir: str = "logs") -> None:
        """
        Logger'ı başlat
        
        Args:
            log_dir: Log dosyalarının depolanacağı dizin
        """
        cls._log_dir = Path(log_dir)
        cls._log_dir.mkdir(exist_ok=True)
        
        # Logger oluştur
        cls._logger = logging.getLogger("SmartNotification")
        cls._logger.setLevel(logging.DEBUG)
        
        # Dosya handler
        log_file = cls._log_dir / f"app_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Handlers ekle
        cls._logger.addHandler(file_handler)
        cls._logger.addHandler(console_handler)
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """Logger instance'ı al"""
        if cls._logger is None:
            cls.initialize()
        return cls._logger
    
    @classmethod
    def info(cls, message: str) -> None:
        """Info level log"""
        cls.get_logger().info(message)
    
    @classmethod
    def debug(cls, message: str) -> None:
        """Debug level log"""
        cls.get_logger().debug(message)
    
    @classmethod
    def warning(cls, message: str) -> None:
        """Warning level log"""
        cls.get_logger().warning(message)
    
    @classmethod
    def error(cls, message: str) -> None:
        """Error level log"""
        cls.get_logger().error(message)
