"""
Главный файл приложения - точка входа
"""
import sys
import asyncio
from pathlib import Path

# Добавляем корневую директорию проекта в путь поиска модулей
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from core.avito_parser import AvitoParser
from core.multi_browser import run_multi_browser_mode
from utils.logger import setup_logger
from config.settings_manager import settings_manager

logger = setup_logger(__name__)


async def run_single_browser_mode():
    """Запуск одного браузера"""
    logger.info("=" * 60)
    logger.info("Запуск Avito Parser (одиночный режим)")
    logger.info("=" * 60)
    
    try:
        async with AvitoParser() as parser:
            result = await parser.parse()
            
            logger.info("=" * 60)
            logger.info("Результаты парсинга:")
            logger.info(f"  Успешно: {result['success']}")
            logger.info(f"  Капча: {'Да' if result['captcha_detected'] else 'Нет'}")
            if result.get('visited_ads'):
                logger.info(f"  Посещено объявлений: {len(result['visited_ads'])}")
                for idx, ad in enumerate(result['visited_ads'], 1):
                    status = "✅" if ad.get('success') else "❌"
                    logger.info(f"    {idx}. {status} {ad['url']}")
            if result.get('error'):
                logger.error(f"  Ошибка: {result['error']}")
            logger.info("=" * 60)
    except Exception as e:
        logger.error(f"Критическая ошибка при выполнении: {e}", exc_info=True)
        return 1
    
    logger.info("Работа завершена успешно")
    return 0


async def main():
    """Главная функция"""
    # Выбираем режим работы в зависимости от настроек
    browser_count = settings_manager.multi_browser.browser_count
    if browser_count > 1:
        logger.info(f"🚀 Мультибраузерный режим: {browser_count} браузеров")
        return await run_multi_browser_mode()
    else:
        logger.info("🔵 Одиночный режим: 1 браузер")
        return await run_single_browser_mode()


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("\n⚠️  Программа прервана пользователем (Ctrl+C)")
        sys.exit(130)
    except Exception as e:
        logger.error(f"💥 Необработанная ошибка: {e}", exc_info=True)
        sys.exit(1)