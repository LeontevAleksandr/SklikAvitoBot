"""
Менеджер для запуска нескольких браузеров одновременно
"""
import asyncio
import random
from typing import List
from core.avito_parser import AvitoParser
from utils.logger import setup_logger
# from config.settings import BROWSERS_COUNT, BROWSER_START_DELAY
from config.settings_manager import settings_manager

logger = setup_logger(__name__)


class MultiBrowserManager:
    """Управление множественными браузерами"""
    
    def __init__(self, browsers_count: int = None):
        """
        Инициализация менеджера
        
        Args:
            browsers_count: Количество браузеров (1-10)
        """
        self.browsers_count = browsers_count or settings_manager.multi_browser.browser_count
        if self.browsers_count < 1:
            self.browsers_count = 1
        if self.browsers_count > 10:
            logger.warning("Максимум 10 браузеров, установлено 10")
            self.browsers_count = 10
        
        logger.info(f"Инициализация {self.browsers_count} браузеров")
    
    async def run_single_browser(self, browser_id: int) -> dict:
        """
        Запускает один браузер
        
        Args:
            browser_id: ID браузера (1-10)
            
        Returns:
            Результат парсинга
        """
        logger.info(f"[Браузер {browser_id}] Запуск...")
        
        try:
            async with AvitoParser() as parser:
                result = await parser.parse()
                result['browser_id'] = browser_id
                
                if result['success']:
                    logger.info(f"[Браузер {browser_id}] ✅ Успешно завершен")
                else:
                    logger.warning(f"[Браузер {browser_id}] ⚠️ Завершен с ошибками")
                
                return result
                
        except Exception as e:
            logger.error(f"[Браузер {browser_id}] ❌ Критическая ошибка: {e}")
            return {
                'browser_id': browser_id,
                'success': False,
                'error': str(e),
                'captcha_detected': False,
                'visited_ads': []
            }
    
    async def run_all_browsers(self) -> List[dict]:
        """
        Запускает все браузеры параллельно
        
        Returns:
            Список результатов от всех браузеров
        """
        logger.info("=" * 60)
        logger.info(f"Запуск {self.browsers_count} браузеров параллельно")
        logger.info("=" * 60)
        
        tasks = []
        
        browser_start_delay = settings_manager.multi_browser.browser_start_delay

        # Создаем задачи для каждого браузера с задержкой
        for i in range(1, self.browsers_count + 1):
            await asyncio.sleep(browser_start_delay)
            
            task = asyncio.create_task(self.run_single_browser(i))
            tasks.append(task)
            
            logger.info(f"Браузер {i}/{self.browsers_count} добавлен в очередь")
        
        # Ждем завершения всех браузеров
        logger.info("Ожидание завершения всех браузеров...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Обрабатываем исключения
        processed_results = []
        for i, result in enumerate(results, 1):
            if isinstance(result, Exception):
                logger.error(f"[Браузер {i}] Исключение: {result}")
                processed_results.append({
                    'browser_id': i,
                    'success': False,
                    'error': str(result),
                    'captcha_detected': False,
                    'visited_ads': []
                })
            else:
                processed_results.append(result)
        
        return processed_results
    
    def print_summary(self, results: List[dict]) -> None:
        """
        Выводит сводку по всем браузерам
        
        Args:
            results: Список результатов
        """
        logger.info("=" * 60)
        logger.info("СВОДКА ПО ВСЕМ БРАУЗЕРАМ")
        logger.info("=" * 60)
        
        total = len(results)
        successful = sum(1 for r in results if r.get('success', False))
        with_captcha = sum(1 for r in results if r.get('captcha_detected', False))
        with_errors = sum(1 for r in results if r.get('error'))
        
        logger.info(f"Всего браузеров: {total}")
        logger.info(f"Успешно: {successful} ({successful/total*100:.1f}%)")
        logger.info(f"С капчей: {with_captcha} ({with_captcha/total*100:.1f}%)")
        logger.info(f"С ошибками: {with_errors} ({with_errors/total*100:.1f}%)")
        
        logger.info("")
        logger.info("Детали по браузерам:")
        
        for result in results:
            browser_id = result.get('browser_id', '?')
            success = result.get('success', False)
            captcha = result.get('captcha_detected', False)
            ads_count = len(result.get('visited_ads', []))
            error = result.get('error', '')
            
            status = "✅" if success else "❌"
            captcha_mark = "🔒" if captcha else ""
            
            logger.info(f"  Браузер {browser_id}: {status} {captcha_mark} | Объявлений: {ads_count}")
            
            if error:
                logger.info(f"    Ошибка: {error[:50]}...")
        
        logger.info("=" * 60)


async def run_multi_browser_mode():
    """
    Запускает режим множественных браузеров
    
    Returns:
        Код возврата (0 - успех, 1 - ошибка)
    """
    manager = MultiBrowserManager()
    
    try:
        results = await manager.run_all_browsers()
        manager.print_summary(results)
        
        # Считаем успешными если хотя бы половина браузеров отработала
        successful = sum(1 for r in results if r.get('success', False))
        if successful >= len(results) / 2:
            logger.info("✅ Задача выполнена успешно")
            return 0
        else:
            logger.warning("⚠️ Менее половины браузеров завершились успешно")
            return 1
            
    except Exception as e:
        logger.error(f"Критическая ошибка в мультибраузерном режиме: {e}", exc_info=True)
        return 1