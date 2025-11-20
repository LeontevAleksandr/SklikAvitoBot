"""
Настройка логирования
"""
import logging
from config.settings_manager import settings_manager


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Настраивает и возвращает логгер
    
    Args:
        name: Имя логгера
        
    Returns:
        Настроенный логгер
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings_manager.logging.level))
    
    # Формат логов
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings_manager.logging.level))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Вывод в файл (опционально)
    log_to_file = settings_manager.logging.to_file
    if log_to_file:
        file_handler = logging.FileHandler(settings_manager.logging.log_file, encoding='utf-8')
        file_handler.setLevel(getattr(logging, settings_manager.logging.level))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger