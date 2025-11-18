"""
Продвинутые настройки для обхода капчи
"""
import random

# TLS Fingerprint - для обхода anti-bot 
# Используем TLS fingerprints
TLS_CIPHERS = [
    'TLS_AES_128_GCM_SHA256',
    'TLS_AES_256_GCM_SHA384',
    'TLS_CHACHA20_POLY1305_SHA256',
    'ECDHE-ECDSA-AES128-GCM-SHA256',
    'ECDHE-RSA-AES128-GCM-SHA256',
]

# Более реалистичные User-Agent с актуальными версиями
REALISTIC_USER_AGENTS = [
    # Chrome на Windows 11
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    # Chrome на Windows 10
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    # Firefox на Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:133.0) Gecko/20100101 Firefox/133.0",
    # Edge на Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
]

# Cookies для имитации возвращающегося пользователя
def get_realistic_cookies():
    """Генерирует реалистичные cookies"""
    return [
        {
            'name': '_ym_uid',
            'value': f"{random.randint(1000000000, 9999999999)}",
            'domain': '.avito.ru',
            'path': '/',
        },
        {
            'name': '_ym_d',
            'value': f"{random.randint(1700000000, 1799999999)}",
            'domain': '.avito.ru',
            'path': '/',
        },
        {
            'name': 'sessid',
            'value': f"{random.randint(100000000, 999999999)}.{random.randint(1000000000, 9999999999)}",
            'domain': '.avito.ru',
            'path': '/',
        }
    ]

# Расширенные заголовки для максимальной реалистичности
def get_advanced_headers(user_agent: str):
    """Возвращает расширенный набор заголовков"""
    return {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'User-Agent': user_agent,
        'DNT': '1',
    }

# Задержки между действиями (увеличены для большей естественности)
REALISTIC_DELAYS = {
    'page_load': (5000, 10000),      # После загрузки страницы
    'scroll': (1500, 3500),          # Между скроллами
    'mouse_move': (300, 800),        # Между движениями мыши
    'click': (500, 1500),            # Перед кликом
    'read_pause': (3000, 8000),      # Пауза "чтения" контента
    'between_requests': (180000, 300000),  # 3-5 минут между запусками!
}

# Список рефереров для имитации перехода с других сайтов
REFERERS = [
    'https://www.google.com/',
    'https://yandex.ru/',
    'https://www.avito.ru/',
    None,  # Прямой переход
]

# Viewport размеры реальных устройств
REAL_VIEWPORTS = [
    {'width': 1920, 'height': 1080},  # Full HD
    {'width': 1366, 'height': 768},   # HD
    {'width': 1536, 'height': 864},   # Laptop
    {'width': 1440, 'height': 900},   # MacBook
    {'width': 1600, 'height': 900},   # Wide
]

# Время суток для запуска (имитация человеческой активности)
# Лучше запускать в часы пик: 9-12, 14-18, 20-22
BEST_HOURS = list(range(9, 12)) + list(range(14, 18)) + list(range(20, 23))

# WebRTC настройки для маскировки
WEBRTC_SETTINGS = {
    'enable_webrtc': True,
    'public_ip': None,  # Будет использован IP прокси
    'local_ip': f'192.168.{random.randint(0, 255)}.{random.randint(1, 254)}',
}