"""
Главное окно приложения
"""
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                            QTabWidget, QLabel)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from config.settings_manager import settings_manager
from .urls import UrlManagerTab
from .settings import SettingsTab
from .parsing import ParsingTab
from .worker import ParserWorker


class AvitoParserGUI(QMainWindow):
    """Главное окно приложения"""
    
    def __init__(self):
        super().__init__()
        self.worker = None
        self.current_settings = {}
        self.setup_ui()
        self.connect_signals()
        
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        self.setWindowTitle("Avito Parser - Накрутка просмотров")
        self.setGeometry(100, 100, 1200, 800)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной layout
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Заголовок
        title_label = QLabel("🚀 Avito Parser - Накрутка просмотров")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #88ccff; margin: 10px;")
        layout.addWidget(title_label)
        
        # TabWidget
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Создаем вкладки
        self.setup_tabs()
        
    def setup_tabs(self):
        """Создает все вкладки приложения"""
        
        # Вкладка парсинга
        self.parsing_tab = ParsingTab()
        self.tab_widget.addTab(self.parsing_tab, "🎯 Парсинг")
        
        # Вкладка URLs
        self.urls_tab = UrlManagerTab()
        self.tab_widget.addTab(self.urls_tab, "🔗 Ссылки")
        
        # Вкладка настроек
        self.settings_tab = SettingsTab()
        self.tab_widget.addTab(self.settings_tab, "⚙️ Настройки")
        
    def connect_signals(self):
        """Подключает сигналы между компонентами"""
        # Сигналы от вкладки парсинга
        self.parsing_tab.start_signal.connect(self.start_parsing)
        self.parsing_tab.stop_signal.connect(self.stop_parsing)
        
        # Сигналы от вкладки URLs
        self.urls_tab.urls_updated.connect(self.on_urls_updated)
        
        # Сигналы от вкладки настроек
        # self.settings_tab.settings_changed.connect(self.on_settings_changed)
        
    def on_urls_updated(self, urls):
        """Обработчик обновления списка ссылок"""
        self.add_log(f"📋 Обновлен список ссылок: {len(urls)} шт", "#888888")
        
    # def on_settings_changed(self, settings):
    #     """Обработчик изменения настроек"""
    #     self.current_settings = settings
    #     self.add_log("⚙️ Настройки обновлены", "#888888")
        
    def start_parsing(self):
        """Запуск парсинга"""
        try:
            # Назначаем текущие настройки
            settings = self.settings_tab.get_settings()
            urls = self.urls_tab.get_urls()
            settings_manager.set_settings(settings, urls)
            
            if not urls:
                self.add_log("❌ Нет ссылок для обработки! Добавьте ссылки во вкладке '🔗 Ссылки'", "#FF4444")
                return    
            
            # Сбрасываем статистику
            self.parsing_tab.get_stats_panel().reset_stats()
            
            # Запускаем воркер
            self.worker = ParserWorker()
            self.worker.log_signal.connect(self.add_log)
            self.worker.finished_signal.connect(self.parsing_finished)
            self.worker.sessions_signal.connect(self.update_sessions)
            self.worker.browsers_signal.connect(self.update_browsers)
            self.worker.stats_signal.connect(self.update_stats)
            self.worker.ip_signal.connect(self.update_ip) 
            self.worker.start()
            
            # Логируем настройки
            browser_settings = settings.get('browsers', {})
            proxy_settings = settings.get('proxy', {})
            
            self.add_log(f"🚀 Запуск парсинга с настройками:", "#4CAF50")
            self.add_log(f"   📊 Браузеров: {browser_settings.get('browser_count', 1)}", "#4CAF50")
            self.add_log(f"   🔗 Ссылок: {len(urls)}", "#4CAF50")
            
            if proxy_settings and proxy_settings.get('server'):
                self.add_log(f"   🌐 Прокси: {proxy_settings['server']}", "#4CAF50")
            else:
                self.add_log("   🌐 Прокси: не используется", "#FFAA00")

            # Обновляем UI
            self.parsing_tab.set_running_state(True)
            
        except Exception as e:
            self.add_log(f"❌ Ошибка запуска: {e}", "#FF4444")
            self.parsing_finished(False)
            
    def add_log(self, message, color="#FFFFFF"):
        """Добавляет сообщение в лог"""
        self.parsing_tab.get_log_widget().append_log(message, color)

    def update_ip(self, ip):
        """Обновление информации по ротациям ip"""
        self.parsing_tab.info_panel.set_ip(ip)

    def update_sessions(self, current: int, total: int):
        """Обновляет счетчик сессий"""
        stats_panel = self.parsing_tab.get_stats_panel()
        stats_panel.update_sessions(current, total)

    def update_browsers(self, current: int, total: int):
        """Обновляет счетчик браузеров"""
        stats_panel = self.parsing_tab.get_stats_panel()
        stats_panel.update_browsers(current, total)

    def update_stats(self, stats_type: str):
        """Обновление статистики"""
        stats_panel = self.parsing_tab.get_stats_panel()
        
        if stats_type == 'view':
            stats_panel.increment_views()
        elif stats_type == 'success':
            stats_panel.increment_success()
        elif stats_type == 'error':
            stats_panel.increment_errors()
        elif stats_type == 'captcha':
            stats_panel.increment_captchas()
            
    def stop_parsing(self):
        """Остановка парсинга"""
        if self.worker and hasattr(self.worker, 'stop') and self.worker.is_running():
            self.worker.stop()
            self.add_log("⏹️ Остановка парсинга...", "#FFAA00")
        else:
            self.parsing_finished(False)
        
    def parsing_finished(self, success):
        """Завершение парсинга"""
        self.parsing_tab.set_running_state(False)
        
        if success:
            self.add_log("✅ Работа завершена успешно", "#4CAF50")
        else:
            self.add_log("❌ Работа завершена с ошибками", "#FF4444")
        
    def closeEvent(self, event):
        """Обработчик закрытия окна"""
        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
        event.accept()
