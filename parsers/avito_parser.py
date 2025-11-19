"""
Парсер Avito
"""
from core.browser import BrowserManager
from core.stealth import apply_stealth
from utils.helpers import random_delay, human_like_scroll, human_like_mouse_movement, random_clicks
from utils.ip_checker import get_current_ip
from utils.logger import setup_logger
from config.settings_manager import settings_manager
from config.settings import TARGET_URL, SCREENSHOTS_DIR, AD_URLS, AD_VIEW_TIME
import asyncio

logger = setup_logger(__name__)


class AvitoParser:
    """Парсер для сайта Avito"""
    
    def __init__(self, url: str = settings_manager.parser.target_url):
        """
        Инициализация парсера
        
        Args:
            url: URL для парсинга
        """
        self.url = url
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
        logger.info(f"Начало парсинга: {self.url}")
        
        result = {
            "success": False,
            "url": self.url,
            "captcha_detected": False,
            "error": None,
            "visited_ads": []
        }
        
        try:
            # Создаем страницу
            page = await self.browser_manager.new_page()
            
            # Применяем stealth техники
            await apply_stealth(page)
            
            # ШАГ 1: Переход на главную страницу
            logger.info(f"Шаг 1: Переход на главную страницу {self.url}")
            await page.goto(self.url, wait_until="domcontentloaded", timeout=30000)
            logger.info("Главная страница загружена")
            
            # Ждем 2 секунды на главной
            await asyncio.sleep(2)
            
            # Проверяем на наличие капчи
            captcha_present = await self.check_captcha(page)
            result["captcha_detected"] = captcha_present
            
            if captcha_present:
                logger.warning("⚠️ ОБНАРУЖЕНА КАПЧА на главной странице!")
                screenshot_path = settings_manager.screenshots_dir / "captcha_main_page.png"
                await page.screenshot(path=str(screenshot_path))
                logger.info(f"Скриншот сохранен: {screenshot_path}")
                await page.close()
                return result
            
            logger.info("✅ Капча не обнаружена на главной странице")
            
            # Быстрая имитация активности на главной
            await human_like_scroll(page)
            
            # ШАГ 2: Посещение объявлений
            ad_urls = settings_manager.parser.ad_urls
            if ad_urls:
                logger.info(f"Шаг 2: Переход к объявлениям (найдено {len(ad_urls)} URL)")
                
                for idx, ad_url in enumerate(ad_urls, 1):
                    logger.info(f"Открытие объявления {idx}/{len(ad_urls)}: {ad_url}")
                    
                    try:
                        # Переход на объявление
                        await page.goto(ad_url, wait_until="domcontentloaded", timeout=30000)
                        logger.info(f"Объявление {idx} загружено")
                        
                        # Ждем 2 секунды после загрузки
                        await asyncio.sleep(2)
                        
                        # Проверка на капчу
                        if await self.check_captcha(page):
                            logger.warning(f"⚠️ КАПЧА на объявлении {idx}!")
                            result["captcha_detected"] = True
                            break
                        
                        logger.info(f"✅ Объявление {idx} открыто успешно")
                        
                        # Быстрый скролл
                        await human_like_scroll(page)
                        
                        # Просмотр объявления
                        ad_view_time = settings_manager.parser.ad_view_time
                        logger.info(f"Просмотр объявления {ad_view_time} секунд...")
                        await asyncio.sleep(ad_view_time)
                        
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
            else:
                logger.info("Объявления для посещения не указаны в ad_urls")
            
            logger.info("Завершена работа со страницами")
            
            result["success"] = True
            await page.close()
            
        except Exception as e:
            logger.error(f"Ошибка при парсинге: {e}")
            result["error"] = str(e)
            
            # Сохраняем скриншот ошибки
            try:
                screenshot_path = settings_manager.screenshots_dir / "error_screenshot.png"
                await page.screenshot(path=str(screenshot_path))
                logger.info(f"Скриншот ошибки сохранен: {screenshot_path}")
            except:
                pass
        
        return result