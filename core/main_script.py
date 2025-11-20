from .avito_parser import AvitoParser
from config.settings_manager import settings_manager
import asyncio
import random
from utils.ip_rotator import rotate_ip
from utils.ip_checker import get_current_ip

async def run_parser():
    """Запуск одного парсера"""
    try:
        async with AvitoParser() as parser:
            result = await parser.parse()
            
            # logger.info("=" * 60)
            # logger.info("Результаты парсинга:")
            # logger.info(f"  Успешно: {result['success']}")
            # logger.info(f"  Капча: {'Да' if result['captcha_detected'] else 'Нет'}")
            if result.get('visited_ads'):
                # logger.info(f"  Посещено объявлений: {len(result['visited_ads'])}")
                for idx, ad in enumerate(result['visited_ads'], 1):
                    status = "✅" if ad.get('success') else "❌"
                    # logger.info(f"    {idx}. {status} {ad['url']}")
            if result.get('error'):
                pass
            #     logger.error(f"  Ошибка: {result['error']}")
            # logger.info("=" * 60)
    except Exception as e:
        return 1
        # logger.error(f"Критическая ошибка при выполнении: {e}", exc_info=True)
    
    # logger.info("Работа завершена успешно")
    return 0

async def start(on_ip=None):
    
    # Количество сессий
    sessions = settings_manager.parser.session
    for session_num in range(sessions):
        # Получение ip и отображение
        ip = get_current_ip()
        if on_ip and ip != "unknown":
            on_ip(ip)

        # Запуск браузеров(парсеров) в текущей сессии
        browser_count = settings_manager.multi_browser.browser_count
        start_delay = settings_manager.multi_browser.browser_start_delay
        tasks = []
        for i in range(browser_count):
            task = asyncio.create_task(run_parser())
            tasks.append(task)
            
            if i < browser_count - 1:
                await asyncio.sleep(start_delay)

        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Вызов IP- ротации у прокси
        rotation_url = settings_manager.proxy.rotation_url
        if rotation_url:
            rotate_ip(rotation_url)

        # Задержка между сессиями (кроме последней)
        if session_num < sessions - 1:
            min_delay = settings_manager.parser.min_delay
            max_delay = settings_manager.parser.max_delay
            delay = random.randint(min_delay, max_delay)
            await asyncio.sleep(delay)