"""
Виджеты для настроек приложения
"""
from PyQt6.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, QLabel, 
                            QSpinBox, QLineEdit, QCheckBox, QPushButton,
                            QComboBox)


class ParserSettingsGroup(QGroupBox):
    """Настройки парсера"""
    
    def __init__(self):
        super().__init__("Настройки парсера")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Режим работы
        mode_layout = QHBoxLayout()
        mode_layout.addWidget(QLabel("Режим работы:"))
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Одиночный запуск", "Непрерывный режим"])
        mode_layout.addWidget(self.mode_combo)
        mode_layout.addStretch()
        layout.addLayout(mode_layout)
        
        # Количество сессий
        sessions_layout = QHBoxLayout()
        sessions_layout.addWidget(QLabel("Количество сессий:"))
        self.sessions_spin = QSpinBox()
        self.sessions_spin.setRange(0, 1000)
        self.sessions_spin.setValue(10)
        self.sessions_spin.setSpecialValueText("бесконечно")
        sessions_layout.addWidget(self.sessions_spin)
        sessions_layout.addStretch()
        layout.addLayout(sessions_layout)
        
        # Задержки между сессиями
        delays_layout = QHBoxLayout()
        delays_layout.addWidget(QLabel("Задержка между сессиями (мин):"))
        self.min_delay_spin = QSpinBox()
        self.min_delay_spin.setRange(1, 60)
        self.min_delay_spin.setValue(2)
        delays_layout.addWidget(self.min_delay_spin)
        
        delays_layout.addWidget(QLabel("до"))
        self.max_delay_spin = QSpinBox()
        self.max_delay_spin.setRange(1, 120)
        self.max_delay_spin.setValue(10)
        delays_layout.addWidget(self.max_delay_spin)
        delays_layout.addStretch()
        layout.addLayout(delays_layout)
        
    def get_settings(self):
        """Возвращает настройки парсера"""
        return {
            'mode': 'continuous' if self.mode_combo.currentText() == "Непрерывный режим" else 'single',
            'sessions': self.sessions_spin.value(),
            'min_delay': self.min_delay_spin.value(),
            'max_delay': self.max_delay_spin.value()
        }


class MultiBrowserSettingsGroup(QGroupBox):
    """Настройки браузеров"""
    
    def __init__(self):
        super().__init__("Настройки браузеров")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Количество браузеров
        browsers_layout = QHBoxLayout()
        browsers_layout.addWidget(QLabel("Количество браузеров:"))
        self.browsers_spin = QSpinBox()
        self.browsers_spin.setRange(1, 10)
        self.browsers_spin.setValue(3)
        self.browsers_spin.setSuffix(" шт")
        browsers_layout.addWidget(self.browsers_spin)
        browsers_layout.addStretch()
        layout.addLayout(browsers_layout)
        
        # Задержка между запусками браузеров
        browser_delay_layout = QHBoxLayout()
        browser_delay_layout.addWidget(QLabel("Задержка между браузерами:"))
        self.browser_delay_spin = QSpinBox()
        self.browser_delay_spin.setRange(10, 300)
        self.browser_delay_spin.setValue(30)
        self.browser_delay_spin.setSuffix(" сек")
        browser_delay_layout.addWidget(self.browser_delay_spin)
        browser_delay_layout.addStretch()
        layout.addLayout(browser_delay_layout)
        
    def get_settings(self):
        """Возвращает настройки браузеров"""
        return {
            'browser_count': self.browsers_spin.value(),
            'browser_start_delay': self.browser_delay_spin.value()
        }


class GeolocationSettings(QGroupBox):
    """Настройки геолокации"""
    
    def __init__(self):
        super().__init__("Настройки геолокации")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Широта
        lat_layout = QHBoxLayout()
        lat_layout.addWidget(QLabel("Широта (lat):"))
        self.lat_input = QLineEdit()
        self.lat_input.setPlaceholderText("55.7558")
        self.lat_input.setText("55.7558")  # Москва по умолчанию
        lat_layout.addWidget(self.lat_input)
        lat_layout.addStretch()
        layout.addLayout(lat_layout)
        
        # Долгота
        lon_layout = QHBoxLayout()
        lon_layout.addWidget(QLabel("Долгота (lon):"))
        self.lon_input = QLineEdit()
        self.lon_input.setPlaceholderText("37.6173")
        self.lon_input.setText("37.6173")  # Москва по умолчанию
        lon_layout.addWidget(self.lon_input)
        lon_layout.addStretch()
        layout.addLayout(lon_layout)
        
        # Кнопка сброса к Москве
        reset_btn = QPushButton("📍 Вернуть значение по умолчанию (Москва)")
        reset_btn.clicked.connect(self.set_moscow)
        layout.addWidget(reset_btn)
        
    def set_moscow(self):
        """Устанавливает координаты Москвы"""
        self.lat_input.setText("55.7558")
        self.lon_input.setText("37.6173")
        # self.timezone.setText("Moscow")
        
    def get_settings(self):
        """Возвращает настройки геолокации"""
        try:
            lat = float(self.lat_input.text().strip())
            lon = float(self.lon_input.text().strip())
            return {'latitude': lat, 'longitude': lon, 'timezone': ''}
        except ValueError:
            return None


class ProxySettingsGroup(QGroupBox):
    """Группа настроек прокси"""
    
    def __init__(self):
        super().__init__("Настройки прокси")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Чекбокс использования прокси
        self.proxy_check = QCheckBox("Использовать прокси (ротация IP)")
        self.proxy_check.setChecked(True)
        self.proxy_check.toggled.connect(self.toggle_proxy_fields)
        layout.addWidget(self.proxy_check)
        
        # Поля для прокси (изначально видимые)
        self.proxy_server_layout = QHBoxLayout()
        self.proxy_server_layout.addWidget(QLabel("Прокси сервер:"))
        self.proxy_server_input = QLineEdit()
        self.proxy_server_input.setPlaceholderText("http://proxy.example.com:8080")
        self.proxy_server_layout.addWidget(self.proxy_server_input)
        layout.addLayout(self.proxy_server_layout)
        
        self.proxy_auth_layout = QHBoxLayout()
        self.proxy_auth_layout.addWidget(QLabel("Логин:"))
        self.proxy_username_input = QLineEdit()
        self.proxy_username_input.setPlaceholderText("username")
        self.proxy_auth_layout.addWidget(self.proxy_username_input)
        
        self.proxy_auth_layout.addWidget(QLabel("Пароль:"))
        self.proxy_password_input = QLineEdit()
        self.proxy_password_input.setPlaceholderText("password")
        self.proxy_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.proxy_auth_layout.addWidget(self.proxy_password_input)
        layout.addLayout(self.proxy_auth_layout)
        
        # Кнопка тестирования прокси
        self.test_proxy_btn = QPushButton("🔍 Тестировать прокси")
        self.test_proxy_btn.clicked.connect(self.test_proxy)
        layout.addWidget(self.test_proxy_btn)
        
    def toggle_proxy_fields(self, enabled):
        """Включает/выключает поля прокси"""
        self.proxy_server_input.setEnabled(enabled)
        self.proxy_username_input.setEnabled(enabled)
        self.proxy_password_input.setEnabled(enabled)
        self.test_proxy_btn.setEnabled(enabled)
        
    def test_proxy(self):
        """Тестирование прокси соединения"""
        # Здесь можно добавить логику тестирования прокси
        print("Тестирование прокси...")
        
    def get_settings(self):
        """Возвращает настройки прокси"""
        if not self.proxy_check.isChecked():
            return None
            
        return {
            'server': self.proxy_server_input.text().strip(),
            'username': self.proxy_username_input.text().strip(),
            'password': self.proxy_password_input.text().strip()
        }
        
    def set_settings(self, server, username="", password=""):
        """Устанавливает настройки прокси"""
        self.proxy_server_input.setText(server)
        self.proxy_username_input.setText(username)
        self.proxy_password_input.setText(password)