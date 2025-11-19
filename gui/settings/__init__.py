"""
Модуль для настроек приложения
"""
from .tab_window import SettingsTab
from .widgets import (MultiBrowserSettingsGroup, GeolocationSettings, 
                     ProxySettingsGroup, ParserSettingsGroup)

__all__ = ['SettingsTab', 'BrowserSettingsGroup', 'GeolocationSettings', 
           'ProxySettingsGroup', 'ParserSettingsGroup']