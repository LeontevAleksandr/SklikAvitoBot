import requests
from typing import Optional

def get_current_ip(
    proxy_server: Optional[str] = None,
    proxy_username: Optional[str] = None,
    proxy_password: Optional[str] = None
) -> str:
    """
    Получает текущий IP через requests
    
    Args:
        proxy_server: URL прокси (http://host:port)
        proxy_username: Логин прокси
        proxy_password: Пароль прокси
        
    Returns:
        IP адрес как строка
    """
    try:
        proxies = {}
        if proxy_server:
            if proxy_username and proxy_password:
                from urllib.parse import quote
                user = quote(proxy_username)
                pwd = quote(proxy_password)
                server = proxy_server.replace('http://', '')
                proxy_url = f"http://{user}:{pwd}@{server}"
            else:
                proxy_url = proxy_server
            
            proxies = {'http': proxy_url, 'https': proxy_url}
        
        response = requests.get("https://api.ipify.org", timeout=10, proxies=proxies)
        return response.text.strip()
        
    except Exception:
        return "unknown"