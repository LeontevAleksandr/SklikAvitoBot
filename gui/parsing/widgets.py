"""
Виджеты для вкладки парсинга
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QGridLayout, QLineEdit)
from PyQt6.QtCore import pyqtSignal


class ControlButtons(QGroupBox):
    """Панель кнопок управления"""
    
    start_signal = pyqtSignal()
    stop_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__("Управление")
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        
        self.start_btn = QPushButton("🚀 Запуск парсинга")
        self.start_btn.clicked.connect(self.start_signal.emit)
        layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹️ Остановить")
        self.stop_btn.clicked.connect(self.stop_signal.emit)
        self.stop_btn.setEnabled(False)
        layout.addWidget(self.stop_btn)
        
    def set_running_state(self, running):
        """Устанавливает состояние кнопок"""
        self.start_btn.setEnabled(not running)
        self.stop_btn.setEnabled(running)


class InfoPanel(QGroupBox):
    """Панель текущей информации по IP"""
    
    def __init__(self):
        super().__init__("Текущий IP")
        self.setup_ui()
        self.ip_change_count = 0
        
    def setup_ui(self):
        layout = QGridLayout(self)
        
        # Текущий IP
        self.ip_label = QLabel("IP: Не определен")
        layout.addWidget(self.ip_label, 0, 0)

        # # Счетчик смен IP
        # self.browsers_label = QLabel("Смен IP: 0")
        # layout.addWidget(self.browsers_label, 0, 1)
        
    def set_ip(self, ip_address: str):
        """Устанавливает текущий IP"""
        self.ip_label.setText(f"IP: {ip_address}")
        
    # def increment_ip_change(self):
    #     """Увеличивает счетчик смен IP"""
    #     self.ip_change_count += 1
    #     self.change_count_label.setText(f"Смен IP: {str(self.ip_change_count)}")
        
    # def reset_counter(self):
    #     """Сбрасывает счетчик"""
    #     self.ip_change_count = 0
    #     self.change_count_label.setText("Смен IP: 0")


class StatsPanel(QGroupBox):
    """Панель статистики"""
    
    def __init__(self):
        super().__init__("Статистика")
        self.setup_ui()
        self.reset_stats()
        
    def setup_ui(self):
        layout = QGridLayout(self)
        
        # Счетчики
        self.sessions_label = QLabel("Сессии: 0")
        layout.addWidget(self.sessions_label, 0, 0)
        
        self.browsers_label = QLabel("Браузеры: 0")
        layout.addWidget(self.browsers_label, 0, 1)
        
        self.views_label = QLabel("Просмотры: 0")
        layout.addWidget(self.views_label, 1, 0)
        
        self.success_label = QLabel("Успешно: 0")
        layout.addWidget(self.success_label, 1, 1)
        
        self.errors_label = QLabel("Ошибки: 0")
        layout.addWidget(self.errors_label, 2, 0)
        
        self.captchas_label = QLabel("Капчи: 0")
        layout.addWidget(self.captchas_label, 2, 1)
        
    def reset_stats(self):
        """Сброс статистики"""
        self.sessions = 0
        self.browsers = 0
        self.views = 0
        self.success = 0
        self.errors = 0
        self.captchas = 0
        self.update_display()
        
    def update_display(self):
        """Обновление отображения"""
        self.sessions_label.setText(f"Сессии: {self.sessions}")
        self.browsers_label.setText(f"Браузеры: {self.browsers}")
        self.views_label.setText(f"Просмотры: {self.views}")
        self.success_label.setText(f"Успешно: {self.success}")
        self.errors_label.setText(f"Ошибки: {self.errors}")
        self.captchas_label.setText(f"Капчи: {self.captchas}")
        
    def increment_sessions(self):
        """Увеличивает счетчик сессий"""
        self.sessions += 1
        self.update_display()
        
    def increment_browsers(self):
        """Увеличивает счетчик браузеров"""
        self.browsers += 1
        self.update_display()
        
    def increment_views(self):
        """Увеличивает счетчик просмотров"""
        self.views += 1
        self.update_display()
        
    def increment_success(self):
        """Увеличивает счетчик успехов"""
        self.success += 1
        self.update_display()
        
    def increment_errors(self):
        """Увеличивает счетчик ошибок"""
        self.errors += 1
        self.update_display()
        
    def increment_captchas(self):
        """Увеличивает счетчик капч"""
        self.captchas += 1
        self.update_display()