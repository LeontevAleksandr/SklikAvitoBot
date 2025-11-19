"""
Вкладка настроек приложения
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt6.QtCore import pyqtSignal, Qt

from .widgets import (ParserSettingsGroup, BrowserSettingsGroup, 
                     GeolocationSettings, ProxySettingsGroup)


class SettingsTab(QWidget):
    """Вкладка настроек"""
    
    settings_changed = pyqtSignal(dict)  # сигнал при изменении настроек
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Scroll Area для настроек
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Контейнер для виджетов настроек
        settings_widget = QWidget()
        settings_layout = QVBoxLayout(settings_widget)
        
        # Группы настроек
        self.parser_group = ParserSettingsGroup()
        settings_layout.addWidget(self.parser_group)
        
        self.browser_group = BrowserSettingsGroup()
        settings_layout.addWidget(self.browser_group)
        
        self.geo_group = GeolocationSettings()
        settings_layout.addWidget(self.geo_group)
        
        self.proxy_group = ProxySettingsGroup()
        settings_layout.addWidget(self.proxy_group)
        
        settings_layout.addStretch()
        
        scroll.setWidget(settings_widget)
        layout.addWidget(scroll)
        
    def get_all_settings(self):
        """Возвращает все настройки"""
        return {
            **self.parser_group.get_parser_settings(),
            'browsers': self.browser_group.get_browser_settings(),
            'geolocation': self.geo_group.get_geolocation(),
            'proxy': self.proxy_group.get_proxy_settings()
        }
        
    def load_proxy_from_env(self):
        """Загружает настройки прокси из переменных окружения"""
        import os
        proxy_server = os.getenv('PROXY_SERVER', '')
        proxy_username = os.getenv('PROXY_USERNAME', '')
        proxy_password = os.getenv('PROXY_PASSWORD', '')
        
        if proxy_server:
            self.proxy_group.set_proxy_settings(proxy_server, proxy_username, proxy_password)