"""
Ротация IP через GET запрос
"""
import requests
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def rotate_ip(rotation_url: str) -> bool:
    """
    Выполняет GET запрос для смены IP
    
    Args:
        rotation_url: URL для ротации IP
        
    Returns:
        True если успешно, False если ошибка
    """
    if not rotation_url:
        return False
    
    try:
        logger.info(f"🔄 Запрос ротации IP: {rotation_url}")
        response = requests.get(rotation_url, timeout=10)
        
        if response.status_code == 200:
            logger.info("✅ IP успешно изменен")
            return True
        else:
            logger.warning(f"⚠️ Ротация IP вернула статус: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error("❌ Таймаут при ротации IP")
        return False
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ Ошибка ротации IP: {e}")
        return False