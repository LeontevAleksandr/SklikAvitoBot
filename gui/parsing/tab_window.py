"""
Вкладка парсинга
"""
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt, pyqtSignal

from .widgets import ControlButtons, StatsPanel
from ..widgets import LogTextEdit


class ParsingTab(QWidget):
    """Вкладка парсинга"""
    
    start_signal = pyqtSignal()
    stop_signal = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Верхняя панель - кнопки управления
        self.control_buttons = ControlButtons()
        self.control_buttons.start_signal.connect(self.start_signal.emit)
        self.control_buttons.stop_signal.connect(self.stop_signal.emit)
        layout.addWidget(self.control_buttons)
        
        # Центральная область - логи
        splitter = QSplitter(Qt.Orientation.Vertical)
        layout.addWidget(splitter)
        
        # Логи
        self.log_text = LogTextEdit()
        splitter.addWidget(self.log_text)
        
        # Статистика
        self.stats_panel = StatsPanel()
        splitter.addWidget(self.stats_panel)
        
        # Пропорции
        splitter.setSizes([400, 100])
        
    def set_running_state(self, running):
        """Устанавливает состояние кнопок"""
        self.control_buttons.set_running_state(running)
        
    def get_stats_panel(self):
        """Возвращает панель статистики"""
        return self.stats_panel
        
    def get_log_widget(self):
        """Возвращает виджет логов"""
        return self.log_text