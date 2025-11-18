"""
Проверка IP адреса
"""
from utils.logger import setup_logger

logger = setup_logger(__name__)


async def get_current_ip(context) -> str:
    """
    Возвращает текущий публичный IP
    
    Args:
        context: Контекст браузера Playwright
        
    Returns:
        JSON строка с информацией об IP или None
    """
    page = await context.new_page()
    try:
        await page.goto("https://api.ipify.org?format=json", wait_until="domcontentloaded")
        ip_data = await page.text_content("body")
        return ip_data
    except Exception as e:
        logger.error(f"Ошибка получения IP: {e}")
        return None
    finally:
        await page.close()