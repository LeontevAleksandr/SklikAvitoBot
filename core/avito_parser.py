"""
Парсер Avito
"""
from core.browser import BrowserManager
from core.stealth import apply_stealth
from utils.logger import setup_logger
from config.settings_manager import settings_manager
import asyncio

logger = setup_logger(__name__)


class AvitoParser:
    """Парсер для сайта Avito"""
    
    def __init__(self, callbacks: dict = None):
        """
        Инициализация парсера
        
        Args:
            url: URL для парсинга
        """
        self.callbacks = callbacks or {}
        self.browser_manager = BrowserManager()
    
    async def __aenter__(self):
        """Асинхронный вход в контекст"""
        await self.browser_manager.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный выход из контекста"""
        await self.browser_manager.close()
    
    async def check_captcha(self, page) -> bool:
        """
        Проверяет наличие капчи на странице
        
        Args:
            page: Объект страницы Playwright
            
        Returns:
            True если капча обнаружена, иначе False
        """
        try:
            captcha_selectors = [
                'iframe[src*="captcha"]',
                'div[class*="captcha"]',
                'div[id*="captcha"]',
                '.captcha-container',
                '#captcha'
            ]
            
            for selector in captcha_selectors:
                count = await page.locator(selector).count()
                if count > 0:
                    return True
            
            return False
        except Exception as e:
            logger.error(f"Ошибка при проверке капчи: {e}")
            return False
    
    async def parse(self) -> dict:
        """
        Основной метод парсинга
        
        Returns:
            Словарь с результатами парсинга
        """
        logger.info(f"Начало парсинга")
        
        result = { # Пока не используется
            "success": False,
            "captcha_detected": False,
            "error": None,
            "visited_ads": []
        }
        
        try:
            # Создаем страницу
            page = await self.browser_manager.new_page()
            
            # Применяем stealth техники
            await apply_stealth(page)
            
            # Посещение объявлений (БЕЗ главной страницы)
            ad_urls = settings_manager.parser.ad_urls
            if ad_urls:
                logger.info(f"Переход к объявлениям (найдено {len(ad_urls)} URL)")
                
                for idx, ad_url in enumerate(ad_urls, 1):
                    logger.info(f"Открытие объявления {idx}/{len(ad_urls)}: {ad_url}")
                    
                    try:
                        # Переход на объявление
                        await page.goto(ad_url, wait_until="domcontentloaded", timeout=30000)
                        logger.info(f"Объявление {idx} загружено")

                        # Тригерим счетчик просмотров
                        if self.callbacks: self.callbacks['on_view']()
                        
                        # Проверка на капчу
                        if await self.check_captcha(page):
                            logger.warning(f"⚠️ КАПЧА на объявлении {idx}!")
                            result["captcha_detected"] = True
                            # Тригерим счетчик капчи
                            if self.callbacks: self.callbacks['on_captcha']()
                            break
                        
                        logger.info(f"✅ Объявление {idx} открыто успешно")
                        
                        # Просмотр объявления
                        ad_view_time = settings_manager.parser.ad_view_time
                        logger.info(f"Просмотр объявления {ad_view_time} секунд...")
                        await asyncio.sleep(ad_view_time)

                        # Тригерим счетчик успешных просмотров
                        if self.callbacks: self.callbacks['on_success']()
                        
                        result["visited_ads"].append({
                            "url": ad_url,
                            "success": True
                        })
                        
                    except Exception as e:
                        logger.error(f"Ошибка при открытии объявления {idx}: {e}")
                        result["visited_ads"].append({
                            "url": ad_url,
                            "success": False,
                            "error": str(e)
                        })
                        # Тригерим счетчик ошибок
                        if self.callbacks: self.callbacks['on_error']()
            else:
                logger.info("Объявления для посещения не указаны")
            
            logger.info("Завершена работа со страницами")
            
            result["success"] = True
            await page.close()
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге: {e}")
            result["error"] = str(e)
            
            # Сохраняем скриншот ошибки
            try:
                screenshot_path = settings_manager.logging.screenshots_dir / "error_screenshot.png"
                await page.screenshot(path=str(screenshot_path))
                logger.info(f"Скриншот ошибки сохранен: {screenshot_path}")
            except:
                pass
        
        return result