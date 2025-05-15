from PyQt6.QtCore import Qt, QAbstractTableModel, QModelIndex
from datetime import datetime

class NotesTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data or []
        self._headers = ['ID', 'Название', 'Содержание', 'Создано', 'Обновлено']

    def rowCount(self, parent=QModelIndex()):
        return len(self._data)

    def columnCount(self, parent=QModelIndex()):
        return len(self._headers)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if not index.isValid():
            return None

        if role == Qt.ItemDataRole.DisplayRole:
            row = index.row()
            col = index.column()
            value = self._data[row][col]

            if col in [3, 4]:  # Форматирование даты
                try:
                    dt = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
                    return dt.strftime("%d.%m.%Y %H:%M")
                except:
                    return value

            if col == 1:  # Ограничение длины названия
                return value[:30] + "..." if len(value) > 30 else value

            if col == 2:  # Ограничение длины содержания
                return value[:50] + "..." if len(value) > 50 else value

            return value

        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self._headers[section]
            if orientation == Qt.Orientation.Vertical:
                return str(section + 1)
        return None

    def update_data(self, data):
        self.beginResetModel()
        self._data = data
        self.endResetModel() 