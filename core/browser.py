"""
Управление браузером
"""
import random
from playwright.async_api import async_playwright, Browser, BrowserContext
from utils.logger import setup_logger
from config.settings_manager import settings_manager


logger = setup_logger(__name__)


class BrowserManager:
    """Менеджер для управления браузером"""
    
    def __init__(self, settings=None):
        self.settings = settings or settings_manager
        self.playwright = None
        self.browser: Browser = None
        self.context: BrowserContext = None
    
    async def __aenter__(self):
        """Асинхронный вход в контекст"""
        await self.start()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Асинхронный выход из контекста"""
        await self.close()
    
    async def start(self) -> None:
        """Запускает браузер и создает контекст"""
        logger.info("Запуск браузера...")
        
        self.playwright = await async_playwright().start()
        
        # Генерируем случайные размеры окна
        viewport_width = random.randint(
            self.settings.browser.viewport_min_width, 
            self.settings.browser.viewport_max_width
        )
        viewport_height = random.randint(
            self.settings.browser.viewport_min_height, 
            self.settings.browser.viewport_max_height
        )

        # Добавляем размер окна к аргументам
        browser_args = self.settings.browser.browser_args.copy()
        browser_args.append(f'--window-size={viewport_width},{viewport_height}')
        
        # Запускаем браузер
        try:
            self.browser = await self.playwright.chromium.launch(
                headless=settings_manager.browser.headless,
                channel="chrome",
                args=browser_args
            )
        except Exception as e:
            logger.warning(f"Не удалось запустить Chrome, используем Chromium: {e}")
            self.browser = await self.playwright.chromium.launch(
                headless=settings_manager.browser.headless,
                args=browser_args
            )
        
        # Настройка прокси
        proxy_config = None
        if settings_manager.proxy.server:
            proxy_config = {"server": settings_manager.proxy.server}
            if settings_manager.proxy.username and settings_manager.proxy.password:
                proxy_config["username"] = settings_manager.proxy.username
                proxy_config["password"] = settings_manager.proxy.password
            logger.info(f"Используется прокси: {settings_manager.proxy.server}")
        
        # Создаем контекст с рандомными параметрами
        self.context = await self.browser.new_context(
            user_agent=random.choice(settings_manager.browser.user_agents),
            viewport={'width': viewport_width, 'height': viewport_height},
            screen={'width': viewport_width, 'height': viewport_height},
            locale='ru-RU',
            # timezone_id=settings_manager.geolocation.timezone,
            permissions=['geolocation'],
            geolocation={
                'longitude': settings_manager.geolocation.longitude,
                'latitude': settings_manager.geolocation.latitude,
                'accuracy': random.randint(5, 50)
            },
            color_scheme='light',
            device_scale_factor=1,
            has_touch=False,
            is_mobile=False,
            java_script_enabled=True,
            extra_http_headers=settings_manager.browser.http_headers,
            proxy=proxy_config
        )
        
        logger.info(f"Браузер запущен (viewport: {viewport_width}x{viewport_height})")
    
    async def new_page(self):
        """
        Создает новую страницу
        
        Returns:
            Объект страницы Playwright
        """
        if not self.context:
            raise RuntimeError("Контекст браузера не создан. Вызовите start() сначала.")
        
        page = await self.context.new_page()
        return page
    
    async def close(self) -> None:
        """Закрывает браузер"""
        if self.context:
            await self.context.close()
            logger.debug("Контекст браузера закрыт")
        
        if self.browser:
            await self.browser.close()
            logger.info("Браузер закрыт")
        
        if self.playwright:
            await self.playwright.stop()
            logger.debug("Playwright остановлен")