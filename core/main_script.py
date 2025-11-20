from .avito_parser import AvitoParser
from config.settings_manager import settings_manager
import asyncio

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


async def start():
    browser_count = settings_manager.multi_browser.browser_count
    start_delay = settings_manager.multi_browser.browser_start_delay
    tasks = []

    for i in range(browser_count):
        task = asyncio.create_task(run_parser())
        tasks.append(task)
    

        if i < browser_count - 1:
            await asyncio.sleep(start_delay)

    results = await asyncio.gather(*tasks, return_exceptions=True)