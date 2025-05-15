import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from main_window import MainWindow
from theme_manager import ThemeManager

def main():
    app = QApplication(sys.argv)
    
    # Установка стиля
    app.setStyle('Fusion')
    
    # Применение начальной темы
    theme_manager = ThemeManager()
    theme_manager.apply_theme(app)
    
    # Создание и отображение главного окна
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 