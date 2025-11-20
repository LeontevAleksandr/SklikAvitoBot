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
    stats_signal = pyqtSignal(str) # stats type: 'session', 'browser', etc.
    ip_rotation_signal = pyqtSignal(str) # Текущий ip

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
        self._is_running = False
        self.log_signal.emit("🛑 Получена команда остановки...", "#FFAA00")
        
    def is_running(self):
        """Проверяет, выполняется ли парсинг"""
        return self._is_running and self.isRunning()
            
    async def _run_async(self):
        """Асинхронная задача"""
        self.log_signal.emit("=" * 60, "#4CAF50")
        self.log_signal.emit("Запуск Avito Parser (одиночный режим)", "#4CAF50")
        self.log_signal.emit("=" * 60, "#4CAF50")
        results = await start(on_ip=self.ip_rotation_signal.emit)