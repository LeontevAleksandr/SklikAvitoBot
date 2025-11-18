"""
Настройки проекта
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Базовые пути
BASE_DIR = Path(__file__).resolve().parent.parent
LOGS_DIR = BASE_DIR / "logs"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"

# Создаем директории если их нет
LOGS_DIR.mkdir(exist_ok=True)
SCREENSHOTS_DIR.mkdir(exist_ok=True)

# Основные настройки
TARGET_URL = os.getenv("TARGET_URL", "https://www.avito.ru/irkutsk")
HEADLESS = os.getenv("HEADLESS", "False").lower() in ("true", "1", "yes")

# Список URL объявлений для посещения
AD_URLS_STR = os.getenv("AD_URLS", "")
AD_URLS = [url.strip() for url in AD_URLS_STR.split(",") if url.strip()]

# Время просмотра объявления (в секундах)
AD_VIEW_TIME = int(os.getenv("AD_VIEW_TIME", "10"))

# Задержки
MIN_DELAY = int(os.getenv("MIN_DELAY", "1000"))
MAX_DELAY = int(os.getenv("MAX_DELAY", "3000"))
MIN_SCROLL_DELAY = int(os.getenv("MIN_SCROLL_DELAY", "800"))
MAX_SCROLL_DELAY = int(os.getenv("MAX_SCROLL_DELAY", "2000"))

# Параметры браузера
VIEWPORT_MIN_WIDTH = int(os.getenv("VIEWPORT_MIN_WIDTH", "1366"))
VIEWPORT_MAX_WIDTH = int(os.getenv("VIEWPORT_MAX_WIDTH", "1920"))
VIEWPORT_MIN_HEIGHT = int(os.getenv("VIEWPORT_MIN_HEIGHT", "768"))
VIEWPORT_MAX_HEIGHT = int(os.getenv("VIEWPORT_MAX_HEIGHT", "1080"))

# Геолокация
GEO_LONGITUDE = float(os.getenv("GEO_LONGITUDE", "104.2964"))
GEO_LATITUDE = float(os.getenv("GEO_LATITUDE", "52.2978"))
TIMEZONE = os.getenv("TIMEZONE", "Asia/Irkutsk")

# Прокси
PROXY_SERVER = os.getenv("PROXY_SERVER")
PROXY_USERNAME = os.getenv("PROXY_USERNAME")
PROXY_PASSWORD = os.getenv("PROXY_PASSWORD")

# Логирование
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_TO_FILE = os.getenv("LOG_TO_FILE", "True").lower() == "true"
LOG_FILE = LOGS_DIR / "parser.log"

# User-Agent список
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
]

# Аргументы браузера
BROWSER_ARGS = [
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
HTTP_HEADERS = {
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