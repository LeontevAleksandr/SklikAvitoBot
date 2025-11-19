"""
Рабочие потоки для GUI
"""
import asyncio
import sys
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal

# Добавляем корневую директорию проекта в путь поиска модулей
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# from main import main_single, main_continuous

class ParserWorker(QThread):
    """Поток для выполнения парсинга"""
    
    log_signal = pyqtSignal(str, str)  # message, color
    finished_signal = pyqtSignal(bool)  # success
    stats_signal = pyqtSignal(str)      # stats type: 'session', 'browser', etc.
    
    def __init__(self, settings, urls):
        super().__init__()
        self.settings = settings
        self.urls = urls
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
        try:
            # Эмулируем работу парсера
            self.stats_signal.emit('session')
            
            browser_count = self.settings.get('browsers', {}).get('browser_count', 1)
            
            for browser_num in range(browser_count):
                if not self._is_running:
                    break
                    
                self.stats_signal.emit('browser')
                self.log_signal.emit(f"🖥️ Запуск браузера {browser_num + 1}", "#4CAF50")
                
                # Обработка URLs для этого браузера
                for url in self.urls:
                    if not self._is_running:
                        break
                        
                    self.stats_signal.emit('view')
                    self.log_signal.emit(f"   📍 Переход по: {url}", "#888888")
                    
                    # Эмуляция работы
                    await asyncio.sleep(1)
                    
                # Задержка между браузерами
                if browser_num < browser_count - 1:
                    delay = self.settings.get('browsers', {}).get('browser_start_delay', 30)
                    self.log_signal.emit(f"⏰ Задержка {delay} сек до следующего браузера", "#FFAA00")
                    await asyncio.sleep(delay)
            
            self.finished_signal.emit(True)
            
        except Exception as e:
            self.log_signal.emit(f"Ошибка выполнения: {e}", "#FF4444")
            self.finished_signal.emit(False)