"""
Вкладка управления URL ссылками
"""
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                            QPushButton, QLabel, QListWidget, QMessageBox)
from PyQt6.QtCore import pyqtSignal

from .widgets import UrlListWidget, UrlImportExport


class UrlManagerTab(QWidget):
    """Вкладка для управления URL ссылками"""
    
    urls_updated = pyqtSignal(list)
    
    def __init__(self):
        super().__init__()
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Панель добавления одиночной ссылки
        self.setup_single_url_section(layout)
        
        # Панель массового импорта
        self.setup_import_section(layout)
        
        # Список ссылок и управление
        self.setup_urls_list_section(layout)
        
        # Статистика
        self.setup_stats_section(layout)
        
    def setup_single_url_section(self, layout):
        """Настраивает секцию добавления одиночного URL"""
        single_url_layout = QHBoxLayout()
        
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Введите URL ссылки (например: https://avito.ru/...)")
        self.url_input.returnPressed.connect(self.add_single_url)
        single_url_layout.addWidget(self.url_input)
        
        self.add_btn = QPushButton("Добавить")
        self.add_btn.clicked.connect(self.add_single_url)
        single_url_layout.addWidget(self.add_btn)
        
        layout.addLayout(single_url_layout)
        
    def setup_import_section(self, layout):
        """Настраивает секцию импорта/экспорта"""
        self.import_export = UrlImportExport()
        self.import_export.urls_imported.connect(self.handle_imported_urls)
        layout.addWidget(self.import_export)
        
    def setup_urls_list_section(self, layout):
        """Настраивает секцию списка URL"""
        urls_layout = QHBoxLayout()
        
        # Левый блок - список
        left_layout = QVBoxLayout()
        left_layout.addWidget(QLabel("Список ссылок:"))
        
        self.urls_list = UrlListWidget()
        self.urls_list.urls_changed.connect(self.handle_urls_changed)
        left_layout.addWidget(self.urls_list)
        
        urls_layout.addLayout(left_layout)
        
        # Правый блок - кнопки управления
        right_layout = QVBoxLayout()
        right_layout.addWidget(QLabel("Действия:"))
        
        self.select_all_btn = QPushButton("✅ Выбрать все")
        self.select_all_btn.clicked.connect(self.urls_list.selectAll)
        right_layout.addWidget(self.select_all_btn)
        
        self.delete_selected_btn = QPushButton("🗑️ Удалить выбранные")
        self.delete_selected_btn.clicked.connect(self.urls_list.remove_selected_urls)
        right_layout.addWidget(self.delete_selected_btn)
        
        self.clear_all_btn = QPushButton("🧹 Очистить все")
        self.clear_all_btn.clicked.connect(self.urls_list.clear_all_urls)
        right_layout.addWidget(self.clear_all_btn)
        
        right_layout.addStretch()
        urls_layout.addLayout(right_layout)
        
        layout.addLayout(urls_layout)
        
    def setup_stats_section(self, layout):
        """Настраивает секцию статистики"""
        self.stats_label = QLabel("Всего ссылок: 0")
        layout.addWidget(self.stats_label)


    # === Обработчики ===    
    def add_single_url(self):
        """Добавляет одиночный URL из поля ввода"""
        url = self.url_input.text().strip()
        if url:
            if self.urls_list.add_url(url):
                self.url_input.clear()
            else:
                QMessageBox.warning(self, "Ошибка", "Некорректный URL или дубликат")
                
    def handle_imported_urls(self, urls):
        """Обрабатывает импортированные URLs"""
        added_count = 0
        for url in urls:
            if self.urls_list.add_url(url):
                added_count += 1
                
        if added_count > 0:
            QMessageBox.information(self, "Успех", f"Добавлено {added_count} URLs")
        else:
            QMessageBox.warning(self, "Предупреждение", "Не удалось добавить ни одного URL")
            
    def handle_urls_changed(self, urls):
        """Обрабатывает изменение списка URLs"""
        self.stats_label.setText(f"Всего ссылок: {len(urls)}")
        self.import_export.export_btn.setEnabled(len(urls) > 0)
        self.urls_updated.emit(urls)
        
    def get_urls(self):
        """Возвращает все URLs"""
        return self.urls_list.get_urls()
        
    def has_urls(self):
        """Проверяет, есть ли URLs"""
        return self.urls_list.count() > 0