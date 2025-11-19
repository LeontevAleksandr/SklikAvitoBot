"""
Общие виджеты для GUI
"""
from PyQt6.QtWidgets import QTextEdit, QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QTextCursor, QPalette, QColor
import logging


class LogHandler(logging.Handler):
    """Кастомный обработчик логов для LogTextEdit"""
    
    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget
        self.setFormatter(logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S"
        ))
    
    def emit(self, record):
        msg = self.format(record)
        
        # Определяем цвет в зависимости от уровня
        if record.levelno >= logging.ERROR:
            color = "#FF4444"  # Красный для ошибок
        elif record.levelno >= logging.WARNING:
            color = "#FFAA00"  # Оранжевый для предупреждений
        elif record.levelno >= logging.INFO:
            color = "#44FF44"  # Зеленый для информации
        else:
            color = "#888888"  # Серый для отладки
            
        self.text_widget.append_log(msg, color)


class LogTextEdit(QTextEdit):
    """Кастомный TextEdit для логов"""
    
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setFont(QFont("Consolas", 9))
        
        # Темная тема для логов
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Base, QColor(30, 30, 30))
        palette.setColor(QPalette.ColorRole.Text, QColor(240, 240, 240))
        self.setPalette(palette)
        
    def append_log(self, message, color="#FFFFFF"):
        """Добавляет сообщение с цветом"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        
        # Форматируем сообщение
        html = f'<span style="color: {color};">{message}</span><br>'
        self.append(html)
        
        # Автопрокрутка
        cursor.movePosition(QTextCursor.MoveOperation.End)
        self.setTextCursor(cursor)
        
        # Ограничение размера логов (последние 1000 строк)
        if self.document().lineCount() > 1000:
            cursor.setPosition(0)
            cursor.movePosition(QTextCursor.MoveOperation.Down, 
                              QTextCursor.MoveMode.KeepAnchor, 100)
            cursor.removeSelectedText()


class StatusBar(QWidget):
    """Строка статуса (если еще нужна)"""
    
    def __init__(self):
        super().__init__()
        from PyQt6.QtWidgets import QHBoxLayout, QLabel, QProgressBar
        
        layout = QHBoxLayout(self)
        
        self.status_label = QLabel("Готов к работе")
        layout.addWidget(self.status_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
    def set_status(self, text, is_working=False):
        """Устанавливает статус"""
        self.status_label.setText(text)
        self.progress_bar.setVisible(is_working)
        
    def set_progress(self, value):
        """Устанавливает прогресс"""
        self.progress_bar.setValue(value)