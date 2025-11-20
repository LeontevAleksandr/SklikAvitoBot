"""
Менеджер настроек приложения
"""
import os
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass, field
from dotenv import load_dotenv


@dataclass
class BrowserSettings:
    """Настройки браузера"""
    headless: bool = False
    viewport_min_width: int = 1366
    viewport_max_width: int = 1920
    viewport_min_height: int = 768
    viewport_max_height: int = 1080
    user_agents: List[str] = field(default_factory=list)
    browser_args: List[str] = field(default_factory=list)
    http_headers: Dict[str, str] = field(default_factory=dict)


@dataclass
class ProxySettings:
    """Настройки прокси"""
    server: str = None
    username: str = None
    password: str = None
    rotation_url: str = None  # URL для ротации IP


@dataclass
class GeolocationSettings:
    """Настройки геолокации"""
    latitude: float = 52.2978  # Иркутск по умолчанию
    longitude: float = 104.2964
    timezone: str = 'Asia/Irkutsk'


@dataclass
class ParserSettings:
    """Настройки парсера"""
    target_url: str = "https://www.avito.ru/irkutsk"
    ad_urls: List[str] = field(default_factory=list)
    ad_view_time: int = 10
    min_delay: int = 500
    max_delay: int = 1000
    min_scroll_delay: int = 400
    max_scroll_delay: int = 800
    session: int = 1


@dataclass
class MultiBrowserSettings:
    """Настройки мультибраузерного режима"""
    browser_count: int = 1
    browser_start_delay: int = 10


@dataclass
class LoggingSettings:
    """Настройки логирования"""
    level: str = "INFO"
    to_file: bool = True
    log_file: Path = None
    logs_dir: Path = None
    screenshots_dir: Path = None


class SettingsManager:
    """Управление настройками приложения"""
    
    def __init__(self):
        # Базовые пути
        self.base_dir = Path(__file__).resolve().parent.parent
        self.logs_dir = self.base_dir / "logs"
        self.screenshots_dir = self.base_dir / "screenshots"
        
        # Создаем директории если их нет
        self.logs_dir.mkdir(exist_ok=True)
        self.screenshots_dir.mkdir(exist_ok=True)
        
        # Инициализируем настройки
        self.browser = BrowserSettings()
        self.proxy = ProxySettings()
        self.geolocation = GeolocationSettings()
        self.parser = ParserSettings()
        self.multi_browser = MultiBrowserSettings()
        self.logging = LoggingSettings()
        
        # Устанавливаем дефолтные значения
        self._set_defaults()
    
    def _set_defaults(self):
        """Устанавливает дефолтные значения"""
        # User-Agents
        self.browser.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        ]
        
        # Аргументы браузера
        self.browser.browser_args = [
            '--disable-blink-features=AutomationControlled',
            '--disable-dev-shm-usage',
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-web-security',
            '--disable-features=IsolateOrigins,site-per-process',
            '--disable-infobars',
            '--disable-background-timer-throttling',
            '--disable-backgrounding-occluded-windows',
            '--disable-renderer-backgrounding',
            '--disable-hang-monitor',
            '--disable-prompt-on-repost',
            '--disable-sync',
            '--disable-translate',
            '--metrics-recording-only',
            '--no-first-run',
            '--safebrowsing-disable-auto-update',
            '--disable-component-update',
            '--disable-default-apps',
            '--disable-domain-reliability',
        ]
        
        # HTTP заголовки
        self.browser.http_headers = {
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-User': '?1',
            'Cache-Control': 'max-age=0',
            'Sec-Ch-Ua': '"Chromium";v="120", "Not_A Brand";v="8", "Google Chrome";v="120"',
            'Sec-Ch-Ua-Mobile': '?0',
            'Sec-Ch-Ua-Platform': '"Windows"',
            'DNT': '1',
        }
        
        # Логирование
        self.logging.logs_dir = self.logs_dir
        self.logging.screenshots_dir = self.screenshots_dir
        self.logging.log_file = self.logs_dir / "parser.log"
    
    def load_from_env(self, env_file: str = ".env"):
        """Загружает настройки из .env файла"""
        load_dotenv(env_file)
        
        # Основные настройки
        self.parser.target_url = os.getenv("TARGET_URL", "https://www.avito.ru/irkutsk")
        self.browser.headless = os.getenv("HEADLESS", "False").lower() in ("true", "1", "yes")
        
        # Список URL объявлений
        ad_urls_str = os.getenv("AD_URLS", "")
        self.parser.ad_urls = [url.strip() for url in ad_urls_str.split(",") if url.strip()]
        
        # Время просмотра
        self.parser.ad_view_time = int(os.getenv("AD_VIEW_TIME", "10"))
        
        # Мультибраузерный режим
        self.multi_browser.browser_count = max(1, min(10, int(os.getenv("BROWSERS_COUNT", "1"))))
        self.multi_browser.browser_start_delay = int(os.getenv("BROWSER_START_DELAY", "2"))
        
        # Задержки
        self.parser.min_delay = int(os.getenv("MIN_DELAY", "1000"))
        self.parser.max_delay = int(os.getenv("MAX_DELAY", "3000"))
        self.parser.min_scroll_delay = int(os.getenv("MIN_SCROLL_DELAY", "800"))
        self.parser.max_scroll_delay = int(os.getenv("MAX_SCROLL_DELAY", "2000"))
        
        # Параметры браузера
        self.browser.viewport_min_width = int(os.getenv("VIEWPORT_MIN_WIDTH", "1366"))
        self.browser.viewport_max_width = int(os.getenv("VIEWPORT_MAX_WIDTH", "1920"))
        self.browser.viewport_min_height = int(os.getenv("VIEWPORT_MIN_HEIGHT", "768"))
        self.browser.viewport_max_height = int(os.getenv("VIEWPORT_MAX_HEIGHT", "1080"))
        
        # Геолокация
        self.geolocation.longitude = float(os.getenv("GEO_LONGITUDE", "104.2964"))
        self.geolocation.latitude = float(os.getenv("GEO_LATITUDE", "52.2978"))
        self.geolocation.timezone = os.getenv("TIMEZONE", "Asia/Irkutsk")
        
        # Прокси
        self.proxy.server = os.getenv("PROXY_SERVER")
        self.proxy.username = os.getenv("PROXY_USERNAME")
        self.proxy.password = os.getenv("PROXY_PASSWORD")
        
        # Логирование
        self.logging.level = os.getenv("LOG_LEVEL", "INFO")
        self.logging.to_file = os.getenv("LOG_TO_FILE", "True").lower() == "true"
    
    def set_settings(self, settings: Dict[str, Any], urls: List[str]):
        """Обновляет настройки из GUI (gui/settings/tab_window)"""
        
        # МультиБраузеры - получаем dict из GUI, обновляем поля объекта
        browsers_dict = settings.get('browsers', {})
        if isinstance(browsers_dict, dict):
            self.multi_browser.browser_count = browsers_dict.get('browser_count', self.multi_browser.browser_count)
            self.multi_browser.browser_start_delay = browsers_dict.get('browser_start_delay', self.multi_browser.browser_start_delay)
        
        # Геолокация - получаем dict из GUI, обновляем поля объекта  
        geo_dict = settings.get('geolocation', {})
        if isinstance(geo_dict, dict):
            self.geolocation.latitude = geo_dict.get('latitude', self.geolocation.latitude)
            self.geolocation.longitude = geo_dict.get('longitude', self.geolocation.longitude)
            # timezone обычно не меняется из GUI, но на всякий случай
            self.geolocation.timezone = geo_dict.get('timezone', self.geolocation.timezone)
        
        # Прокси - получаем dict или None из GUI
        proxy_dict = settings.get('proxy')
        if proxy_dict and isinstance(proxy_dict, dict):
            # Если прокси включен в GUI
            self.proxy.server = proxy_dict.get('server')
            self.proxy.username = proxy_dict.get('username', '')
            self.proxy.password = proxy_dict.get('password', '')
            self.proxy.rotation_url = proxy_dict.get('rotation_url', '')
        else:
            # Если прокси отключен в GUI
            self.proxy.server = None
            self.proxy.username = None
            self.proxy.password = None
            self.proxy.rotation_url = None
        
        
        # Остальные настройки парсера
        self.parser.session = settings.get('sessions', self.parser.session)
        self.parser.min_delay = settings.get('min_delay', ParserSettings.min_delay)
        self.parser.max_delay = settings.get('max_delay', ParserSettings.max_delay)
        self.parser.ad_urls = urls


# Глобальный экземпляр настроек
settings_manager = SettingsManager()

# Загружаем настройки из .env при импорте
# settings_manager.load_from_env()