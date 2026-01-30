"""
Вкладка настроек приложения
"""
import json
from pathlib import Path
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout
from PyQt6.QtCore import pyqtSignal, Qt

from .widgets import (ParserSettingsGroup, MultiBrowserSettingsGroup, 
                     GeolocationSettings, ProxySettingsGroup)


class SettingsTab(QWidget):
    """Вкладка настроек"""
    
    settings_changed = pyqtSignal(dict)  # сигнал при изменении настроек
    
    SETTINGS_FILE = Path("settings.json")
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_settings()
        
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
        
        self.multibrowser_group = MultiBrowserSettingsGroup()
        settings_layout.addWidget(self.multibrowser_group)
        
        self.geo_group = GeolocationSettings()
        settings_layout.addWidget(self.geo_group)
        
        self.proxy_group = ProxySettingsGroup()
        settings_layout.addWidget(self.proxy_group)
        
        settings_layout.addStretch()
        
        scroll.setWidget(settings_widget)
        layout.addWidget(scroll)
        
        # Кнопки управления
        buttons_layout = QHBoxLayout()
        
        save_btn = QPushButton("💾 Сохранить настройки")
        save_btn.clicked.connect(self.save_settings)
        buttons_layout.addWidget(save_btn)
        
        load_btn = QPushButton("📂 Загрузить настройки")
        load_btn.clicked.connect(self.load_settings)
        buttons_layout.addWidget(load_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
    def get_settings(self):
        """Возвращает все настройки"""
        return {
            **self.parser_group.get_settings(),
            'browsers': self.multibrowser_group.get_settings(),
            'geolocation': self.geo_group.get_settings(),
            'proxy': self.proxy_group.get_settings()
        }
    
    def save_settings(self):
        """Сохраняет настройки в JSON файл"""
        settings = self.get_settings()
        try:
            with open(self.SETTINGS_FILE, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2, ensure_ascii=False)
            self.settings_changed.emit(settings)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {e}")
    
    def load_settings(self):
        """Загружает настройки из JSON файла"""
        if not self.SETTINGS_FILE.exists():
            return
        
        try:
            with open(self.SETTINGS_FILE, 'r', encoding='utf-8') as f:
                settings = json.load(f)
            
            # Настройки парсера
            if 'ad_view_time' in settings:
                self.parser_group.time_spin.setValue(settings['ad_view_time'])
            if 'sessions' in settings:
                self.parser_group.sessions_spin.setValue(settings['sessions'])
            if 'min_delay' in settings:
                self.parser_group.min_delay_spin.setValue(settings['min_delay'])
            if 'max_delay' in settings:
                self.parser_group.max_delay_spin.setValue(settings['max_delay'])
            
            # Настройки браузеров
            if 'browsers' in settings:
                browsers = settings['browsers']
                if 'browser_count' in browsers:
                    self.multibrowser_group.browsers_spin.setValue(browsers['browser_count'])
                if 'browser_start_delay' in browsers:
                    self.multibrowser_group.browser_delay_spin.setValue(browsers['browser_start_delay'])
            
            # Геолокация
            if 'geolocation' in settings and settings['geolocation']:
                geo = settings['geolocation']
                if 'latitude' in geo:
                    self.geo_group.lat_input.setText(str(geo['latitude']))
                if 'longitude' in geo:
                    self.geo_group.lon_input.setText(str(geo['longitude']))
            
            # Прокси
            if 'proxy' in settings and settings['proxy']:
                proxy = settings['proxy']
                self.proxy_group.proxy_check.setChecked(True)
                if 'server' in proxy:
                    self.proxy_group.proxy_server_input.setText(proxy['server'])
                if 'username' in proxy:
                    self.proxy_group.proxy_username_input.setText(proxy['username'])
                if 'password' in proxy:
                    self.proxy_group.proxy_password_input.setText(proxy['password'])
                if 'rotation_url' in proxy:
                    self.proxy_group.rotation_check.setChecked(True)
                    self.proxy_group.rotation_url_input.setText(proxy['rotation_url'])
            else:
                self.proxy_group.proxy_check.setChecked(False)
                
        except Exception as e:
            print(f"Ошибка загрузки настроек: {e}")