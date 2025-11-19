"""
Рабочие потоки для GUI
"""
import asyncio
import sys
from pathlib import Path
from PyQt6.QtCore import QThread, pyqtSignal
from parsers.avito_parser import AvitoParser
import traceback

# Добавляем корневую директорию проекта в путь поиска модулей
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# from main import main_single, main_continuous

class ParserWorker(QThread):
    """Поток для выполнения парсинга"""
    
    log_signal = pyqtSignal(str, str)  # message, color
    finished_signal = pyqtSignal(bool)  # success
    stats_signal = pyqtSignal(str)      # stats type: 'session', 'browser', etc.
    
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
        
        try:
            async with AvitoParser() as parser:
                result = await parser.parse()
                self.log_signal.emit("=" * 60, "#4CAF50")
                self.log_signal.emit("Результаты парсинга:", "#4CAF50")
                self.log_signal.emit(f"  Успешно: {result['success']}", "#4CAF50")
                self.log_signal.emit(f"  Капча: {'Да' if result['captcha_detected'] else 'Нет'}", "#4CAF50")
                if result.get('visited_ads'):
                    self.log_signal.emit("  Посещено объявлений: {len(result['visited_ads'])}", "#4CAF50")
                    for idx, ad in enumerate(result['visited_ads'], 1):
                        status = "✅" if ad.get('success') else "❌"
                        self.log_signal.emit(f"    {idx}. {status} {ad['url']}", "#4CAF50")
                if result.get('error'):
                    self.log_signal.emit(f"  Ошибка: {result['error']}", "#FF4444")
                self.log_signal.emit("=" * 60, "#4CAF50")
        except Exception as e:

            error_traceback = traceback.format_exc()
            self.log_signal.emit(f"❌ Критическая ошибка:", "#FF4444")
            self.log_signal.emit(f"📋 Сообщение: {str(e)}", "#FF4444")
            self.log_signal.emit(f"🔍 Traceback:", "#FF4444")

            # Разбиваем traceback на строки и логируем каждую
            for line in error_traceback.split('\n'):
                if line.strip():
                    self.log_signal.emit(f"   {line}", "#FF8888")
            
            self.finished_signal.emit(False)

            # self.log_signal.emit(f"Критическая ошибка при выполнении: {e}", "#FF4444")
            self.finished_signal.emit(True)
            return 1
        self.log_signal.emit("Работа завершена успешно", "#4CAF50")
        return 0