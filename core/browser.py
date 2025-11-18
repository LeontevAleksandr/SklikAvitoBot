"""
Управление браузером
"""
import random
from playwright.async_api import async_playwright, Browser, BrowserContext
from config.settings import (
    HEADLESS, BROWSER_ARGS, USER_AGENTS, HTTP_HEADERS,
    VIEWPORT_MIN_WIDTH, VIEWPORT_MAX_WIDTH, VIEWPORT_MIN_HEIGHT, VIEWPORT_MAX_HEIGHT,
    GEO_LONGITUDE, GEO_LATITUDE, TIMEZONE,
    PROXY_SERVER, PROXY_USERNAME, PROXY_PASSWORD
)
from utils.logger import setup_logger

logger = setup_logger(__name__)


class BrowserManager:
    """Менеджер для управления браузером"""
    
    def __init__(self):
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
        viewport_width = random.randint(VIEWPORT_MIN_WIDTH, VIEWPORT_MAX_WIDTH)
        viewport_height = random.randint(VIEWPORT_MIN_HEIGHT, VIEWPORT_MAX_HEIGHT)
        
        # Добавляем размер окна к аргументам
        browser_args = BROWSER_ARGS.copy()
        browser_args.append(f'--window-size={viewport_width},{viewport_height}')
        
        # Запускаем браузер
        try:
            self.browser = await self.playwright.chromium.launch(
                headless=HEADLESS,
                channel="chrome",
                args=browser_args
            )
        except Exception as e:
            logger.warning(f"Не удалось запустить Chrome, используем Chromium: {e}")
            self.browser = await self.playwright.chromium.launch(
                headless=HEADLESS,
                args=browser_args
            )
        
        # Настройка прокси
        proxy_config = None
        if PROXY_SERVER:
            proxy_config = {"server": PROXY_SERVER}
            if PROXY_USERNAME and PROXY_PASSWORD:
                proxy_config["username"] = PROXY_USERNAME
                proxy_config["password"] = PROXY_PASSWORD
            logger.info(f"Используется прокси: {PROXY_SERVER}")
        
        # Создаем контекст с рандомными параметрами
        self.context = await self.browser.new_context(
            user_agent=random.choice(USER_AGENTS),
            viewport={'width': viewport_width, 'height': viewport_height},
            screen={'width': viewport_width, 'height': viewport_height},
            locale='ru-RU',
            timezone_id=TIMEZONE,
            permissions=['geolocation'],
            geolocation={
                'longitude': GEO_LONGITUDE,
                'latitude': GEO_LATITUDE,
                'accuracy': random.randint(5, 50)
            },
            color_scheme='light',
            device_scale_factor=1,
            has_touch=False,
            is_mobile=False,
            java_script_enabled=True,
            extra_http_headers=HTTP_HEADERS,
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