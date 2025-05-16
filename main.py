import sys
import os
from PyQt5.QtWidgets import QApplication
from ui.main_window import MainWindow

if __name__ == "__main__":
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    UI_DIR = os.path.join(BASE_DIR, "ui")

    
    main_window_ui_path = os.path.join(UI_DIR, "main_window.ui")
    if not os.path.exists(main_window_ui_path):
        raise FileNotFoundError(f"Файл {main_window_ui_path} не найден! Проверьте расположение!")

    
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

