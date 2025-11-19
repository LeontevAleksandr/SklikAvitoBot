"""
Виджеты для работы с URL ссылками
"""
from PyQt6.QtWidgets import (QListWidget, QPushButton, 
                            QHBoxLayout, QWidget, QListWidgetItem, 
                            QFileDialog, QMessageBox)
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QFont


class UrlListWidget(QListWidget):
    """Кастомный список URL с проверкой валидности"""
    
    urls_changed = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.setFont(QFont("Consolas", 9))
        
    def add_url(self, url):
        """Добавляет URL с проверкой"""
        url = url.strip()
        if self.is_valid_url(url) and not self.is_duplicate(url):
            item = QListWidgetItem(url)
            self.addItem(item)
            self.urls_changed.emit(self.get_all_urls())
            return True
        return False
        
    def is_valid_url(self, url):
        """Проверяет валидность URL"""
        return url.startswith(('http://', 'https://')) and len(url) > 10
        
    def is_duplicate(self, url):
        """Проверяет дубликат URL"""
        for i in range(self.count()):
            if self.item(i).text() == url:
                return True
        return False
        
    def get_all_urls(self):
        """Возвращает все URLs"""
        return [self.item(i).text() for i in range(self.count())]
        
    def remove_selected_urls(self):
        """Удаляет выбранные URLs"""
        for item in self.selectedItems():
            self.takeItem(self.row(item))
        self.urls_changed.emit(self.get_all_urls())
        
    def clear_all_urls(self):
        """Очищает все URLs"""
        self.clear()
        self.urls_changed.emit([])


class UrlImportExport(QWidget):
    """Виджет для импорта/экспорта URLs"""
    
    urls_imported = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QHBoxLayout(self)
        
        self.import_btn = QPushButton("📁 Импорт из файла")
        self.import_btn.clicked.connect(self.import_urls)
        layout.addWidget(self.import_btn)
        
        self.paste_btn = QPushButton("📋 Вставить из буфера")
        self.paste_btn.clicked.connect(self.paste_urls)
        layout.addWidget(self.paste_btn)
        
        self.export_btn = QPushButton("💾 Экспорт в файл")
        self.export_btn.clicked.connect(self.export_urls)
        layout.addWidget(self.export_btn)
        
    def import_urls(self):
        """Импортирует URLs из файла"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Выберите файл с URLs", "", "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    urls = [line.strip() for line in f if line.strip()]
                self.urls_imported.emit(urls)
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить файл: {e}")
                
    def paste_urls(self):
        """Импортирует URLs из буфера обмена"""
        from PyQt6.QtWidgets import QApplication
        clipboard = QApplication.clipboard()
        text = clipboard.text().strip()
        
        if text:
            urls = [url.strip() for url in text.split('\n') if url.strip()]
            self.urls_imported.emit(urls)
            
    def export_urls(self, urls):
        """Экспортирует URLs в файл"""
        if not urls:
            QMessageBox.warning(self, "Предупреждение", "Нет URLs для экспорта")
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить URLs", "urls.txt", "Text Files (*.txt)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    for url in urls:
                        f.write(url + '\n')
                QMessageBox.information(self, "Успешно", f"URLs сохранены в {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Ошибка", f"Не удалось сохранить файл: {e}")