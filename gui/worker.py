"""
Рабочие потоки для GUI
"""
import asyncio
import sys
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal
import traceback
from core.main_script import start

# Добавляем корневую директорию проекта в путь поиска модулей
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

class ParserWorker(QThread):
    """Поток для выполнения парсинга"""
    
    log_signal = pyqtSignal(str, str) # message, color
    finished_signal = pyqtSignal(bool) # success
    sessions_signal = pyqtSignal(int, int)
    browsers_signal = pyqtSignal(int, int)
    stats_signal = pyqtSignal(str) # stats type: 'view', 'errors', etc.
    ip_signal = pyqtSignal(str) # Текущий ip

    def __init__(self):
        super().__init__()
        self._is_running = True
        
    def run(self):
        """Запуск асинхронной задачи"""
        try:
            asyncio.run(self._run_async())
        except Exception as e:
            self.log_signal.emit(f"Ошибка потока: {e}", "#FF4444")
            self.finished_signal.emit(False)

    def stop(self):
        """Останавливает выполнение парсинга"""
        if not self._is_running:
            return  # Уже остановлен

        self._is_running = False
        self.log_signal.emit("🛑 Получена команда остановки, ожидаем завершения...", "#FFAA00")
        
    def is_running(self):
        """Проверяет, выполняется ли парсинг"""
        return self._is_running and self.isRunning()
            
    async def _run_async(self):
        """Асинхронная задача"""
        self.log_signal.emit("=" * 60, "#4CAF50")
        self.log_signal.emit("Запуск Avito Parser", "#4CAF50")
        self.log_signal.emit("=" * 60, "#4CAF50")

        callbacks = {
            'on_session': self.update_sessions,
            'on_browser': self.update_browsers,
            'on_view': self.increment_views,
            'on_success': self.increment_success,
            'on_error': self.increment_errors,
            'on_ip': self.rotate_ip,
            'should_stop': lambda: not self._is_running  # Функция проверки остановки
        }

        try:
            results = await start(callbacks)
            self.finished_signal.emit(True)
        except asyncio.CancelledError:
            self.log_signal.emit("🛑 Парсинг прерван пользователем", "#FFAA00")
            self.finished_signal.emit(False)
        except Exception as e:
            self.log_signal.emit(f"❌ Ошибка парсинга: {e}", "#FF4444")
            self.finished_signal.emit(False)
    
    # Функции для коллбэков
    def update_sessions(self, current, total):
        self.sessions_signal.emit(current, total)

    def update_browsers(self, current, total):
        self.browsers_signal.emit(current, total)

    def increment_views(self):
        self.stats_signal.emit('view')
    
    def increment_success(self):
        self.stats_signal.emit('success')
    
    def increment_errors(self):
        self.stats_signal.emit('error')

    def increment_captcha(self):
        self.stats_signal.emit('captcha')

    def rotate_ip(self, ip):
        self.ip_signal.emit(ip)