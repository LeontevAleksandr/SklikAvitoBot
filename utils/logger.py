"""
Настройка логирования
"""
import logging
from config.settings import LOG_LEVEL, LOG_TO_FILE, LOG_FILE


def setup_logger(name: str = __name__) -> logging.Logger:
    """
    Настраивает и возвращает логгер
    
    Args:
        name: Имя логгера
        
    Returns:
        Настроенный логгер
    """
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # Формат логов
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Вывод в консоль
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Вывод в файл (опционально)
    if LOG_TO_FILE:
        file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    return logger