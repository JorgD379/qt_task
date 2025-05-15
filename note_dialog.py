from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, 
                             QLabel, QLineEdit, QTextEdit, QPushButton)
from PyQt6.QtCore import Qt

class NoteDialog(QDialog):
    def __init__(self, parent=None, note_data=None):
        super().__init__(parent)
        self.note_data = note_data
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Редактирование заметки" if self.note_data else "Новая заметка")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)

        layout = QVBoxLayout()

        # Название
        title_layout = QHBoxLayout()
        title_label = QLabel("Название:")
        self.title_edit = QLineEdit()
        self.title_edit.setMaxLength(50)
        title_layout.addWidget(title_label)
        title_layout.addWidget(self.title_edit)
        layout.addLayout(title_layout)

        # Содержание
        content_label = QLabel("Содержание:")
        self.content_edit = QTextEdit()
        layout.addWidget(content_label)
        layout.addWidget(self.content_edit)

        # Кнопки
        button_layout = QHBoxLayout()
        self.save_button = QPushButton("Сохранить")
        self.cancel_button = QPushButton("Отмена")
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Подключение сигналов
        self.save_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # Заполнение данных, если это редактирование
        if self.note_data:
            self.title_edit.setText(self.note_data[1])  # title
            self.content_edit.setText(self.note_data[2])  # content

    def get_note_data(self):
        return {
            'title': self.title_edit.text().strip(),
            'content': self.content_edit.toPlainText().strip()
        } 