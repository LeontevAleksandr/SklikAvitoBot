from .avito_parser import AvitoParser
from config.settings_manager import settings_manager
import asyncio

async def run_parser():
    """Запуск одного парсера"""
    try:
        async with AvitoParser() as parser:
            result = await parser.parse()
            
            if result.get('visited_ads'):
                for idx, ad in enumerate(result['visited_ads'], 1):
                    status = "✅" if ad.get('success') else "❌"
                    
            if result.get('error'):
                pass
            
    except Exception as e:
        return 1
    
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