from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QTableView, QMessageBox, QLineEdit,
                             QComboBox, QApplication)
from PyQt6.QtCore import Qt
from database import Database
from models import NotesTableModel
from note_dialog import NoteDialog
from theme_manager import ThemeManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.theme_manager = ThemeManager()
        self.setup_ui()
        self.load_notes()

    def setup_ui(self):
        self.setWindowTitle("Заметки")
        self.setMinimumSize(800, 600)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Поиск и сортировка
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Поиск по названию...")
        self.search_input.textChanged.connect(self.search_notes)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["По дате обновления", "По дате создания"])
        self.sort_combo.currentIndexChanged.connect(self.load_notes)
        
        self.theme_button = QPushButton("🌙 Сменить тему")
        self.theme_button.clicked.connect(self.toggle_theme)
        
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.sort_combo)
        search_layout.addWidget(self.theme_button)
        layout.addLayout(search_layout)

        # Таблица
        self.table = QTableView()
        self.table.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableView.SelectionMode.SingleSelection)
        layout.addWidget(self.table)

        # Кнопки
        button_layout = QHBoxLayout()
        self.create_button = QPushButton("Создать")
        self.edit_button = QPushButton("Редактировать")
        self.delete_button = QPushButton("Удалить")
        self.refresh_button = QPushButton("Обновить")

        button_layout.addWidget(self.create_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.refresh_button)
        layout.addLayout(button_layout)

        # Подключение сигналов
        self.create_button.clicked.connect(self.create_note)
        self.edit_button.clicked.connect(self.edit_note)
        self.delete_button.clicked.connect(self.delete_note)
        self.refresh_button.clicked.connect(self.load_notes)

    def toggle_theme(self):
        is_dark = self.theme_manager.toggle_theme()
        self.theme_button.setText("☀️ Сменить тему" if is_dark else "🌙 Сменить тему")
        self.theme_manager.apply_theme(QApplication.instance())

    def load_notes(self):
        notes = self.db.get_all_notes()
        if self.sort_combo.currentIndex() == 1:  # По дате создания
            notes.sort(key=lambda x: x[3])  # created_at
        self.model = NotesTableModel(notes)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    def search_notes(self):
        query = self.search_input.text()
        if query:
            notes = self.db.search_notes(query)
        else:
            notes = self.db.get_all_notes()
        self.model = NotesTableModel(notes)
        self.table.setModel(self.model)
        self.table.resizeColumnsToContents()

    def create_note(self):
        dialog = NoteDialog(self)
        if dialog.exec():
            note_data = dialog.get_note_data()
            if note_data['title']:
                self.db.add_note(note_data['title'], note_data['content'])
                self.load_notes()
            else:
                QMessageBox.warning(self, "Ошибка", "Название не может быть пустым")

    def edit_note(self):
        indexes = self.table.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, "Ошибка", "Выберите заметку для редактирования")
            return

        row = indexes[0].row()
        note_id = self.model._data[row][0]
        note_data = self.db.get_note(note_id)

        dialog = NoteDialog(self, note_data)
        if dialog.exec():
            note_data = dialog.get_note_data()
            if note_data['title']:
                self.db.update_note(note_id, note_data['title'], note_data['content'])
                self.load_notes()
            else:
                QMessageBox.warning(self, "Ошибка", "Название не может быть пустым")

    def delete_note(self):
        indexes = self.table.selectedIndexes()
        if not indexes:
            QMessageBox.warning(self, "Ошибка", "Выберите заметку для удаления")
            return

        reply = QMessageBox.question(
            self, "Подтверждение",
            "Вы уверены, что хотите удалить эту заметку?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            row = indexes[0].row()
            note_id = self.model._data[row][0]
            self.db.delete_note(note_id)
            self.load_notes() 