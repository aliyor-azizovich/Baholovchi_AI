import os
from PyQt5 import uic
from PyQt5.QtGui import QIcon
import shutil

from PyQt5.QtWidgets import (QMainWindow, QPushButton, QTableWidget, QAbstractItemView, QTableWidgetItem, QHeaderView, QFileDialog,
        QMessageBox, QMenu, QLabel, QLineEdit, QListWidget)
from PyQt5.QtCore import Qt, QDate
from ui.new_report import NewReportWindow
import json
from logic.ReportRegistry import ReportRegistry
from ui.valuation_main import ValuationMainWindow
from logic.ReportFileManager import ReportFileManager

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.project_dir = os.path.dirname(BASE_DIR)  
        ui_path = os.path.join(self.project_dir, "ui", "main_window.ui")
        uic.loadUi(ui_path, self)
        self.load_settings()

        
        self.setWindowTitle("AICostMaster")
        self.setWindowIcon(QIcon("icon_change.png"))  
        self.showMaximized()
       
        # Создаём объект для работы с файлами отчёта
        self.report_manager = ReportFileManager(self.project_dir)

        # Создаём объект для работы с реестром
        self.report_registry = ReportRegistry(self.project_dir) 
        self.saved_liters = []

        self.save_dir = self.findChild(QMenu, "save_dir") 
        self.action_dir.triggered.connect(self.select_save_directory) #определяем место хранения Word варинатов отчёта

        self.search_layer = self.findChild(QLineEdit, 'search_layer')
        self.search_layer.textChanged.connect(self.search_reports)

        self.sortirovshik_po_datam = self.findChild(QListWidget, 'sortirovshik_po_datam')
        self.sortirovshik_po_datam.currentTextChanged.connect(self.filter_by_date_range)


        headers = ['', '', 'Рег№ отчёта', 'Дата регистрации', 'Дата последнего изменения', 'Владелец', 
                   'Заказчик', 'Адрес объекта', 'Оценочная стоимость'] # Заголовки столбцов таблицы MainTableForDocs
        self.report_table = self.findChild(QTableWidget, "MainTableForDocs")
        self.report_table.setColumnCount(len(headers))
        self.report_table.setHorizontalHeaderLabels(headers)
        self.report_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.report_table.setSelectionBehavior(QTableWidget.SelectRows)  # Выделение всей строки
        self.report_table.setSelectionMode(QAbstractItemView.SingleSelection)  # Одна строка за раз
        self.report_table.setColumnWidth(0, 15) 
        self.report_table.setColumnHidden(1, True)

        self.report_table.itemDoubleClicked.connect(self.open_report)

        # Привязываем кнопки к методам копирования и удаления
        self.copy_button = self.findChild(QPushButton, "copy_button")
        self.delete_button = self.findChild(QPushButton, "delete_button")
        self.copy_button.clicked.connect(self.copy_selected_reports)
        self.delete_button.clicked.connect(self.delete_selected_reports)

        # Вызываем метод загрузки отчётов из реестра
        self.load_reports_from_registry()

        # кнопка добаления нового отчёта
        self.add_report_button = self.findChild(QPushButton, "New_doc_Button")
        self.add_report_button.clicked.connect(self.open_new_report)
            


    def filter_by_date_range(self, selected_text):
        today = QDate.currentDate()

        for row in range(self.report_table.rowCount()):
            date_item = self.report_table.item(row, 3)  # колонка "Дата регистрации"
            if not date_item:
                self.report_table.setRowHidden(row, True)
                continue

            try:
                report_date = QDate.fromString(date_item.text(), "yyyy-MM-dd")
            except Exception:
                self.report_table.setRowHidden(row, True)
                continue

            show_row = True
            if selected_text == "За месяц":
                show_row = report_date.daysTo(today) <= 31
            elif selected_text == "2025":
                show_row = report_date.year() == 2025
            elif selected_text == "Все":
                show_row = True
            elif selected_text == "2024":
                show_row = report_date.year() == 2024
            else:
                show_row = True  # запасной вариант

            self.report_table.setRowHidden(row, not show_row)
        

    def search_reports(self, text):
        text = text.strip().lower()

        # Очищаем фильтр, если меньше 3 символов
        if len(text) < 3:
            for row in range(self.report_table.rowCount()):
                self.report_table.setRowHidden(row, False)
            return

        # Иначе фильтруем строки
        for row in range(self.report_table.rowCount()):
            owner_item = self.report_table.item(row, 5)  # Владелец
            buyer_item = self.report_table.item(row, 6)  # Заказчик
            address_item = self.report_table.item(row, 7)  # Адрес объекта

            owner_text = owner_item.text().lower() if owner_item else ""
            buyer_text = buyer_item.text().lower() if buyer_item else ""
            address_text = address_item.text().lower() if address_item else ""

            # Проверяем наличие текста в любом из полей
            match = (text in owner_text) or (text in buyer_text) or (text in address_text)

            self.report_table.setRowHidden(row, not match)





           
    # Добавляем отчёту уникальный идентификатор путём max_number + 1 
    def get_last_report_number(self):
        try:
            # Загружаем данные из реестра
            data = self.report_registry.load_registry()
            reports = data.get("reports", [])

            max_number = 0

            # Перебираем все отчеты из файла
            for report in reports:
                report_number = report.get("report_number", "")
                try:
                    number = int(report_number)
                    if number > max_number:
                        max_number = number
                except ValueError:
                    # Игнорируем, если не удалось преобразовать в число
                    continue

            # Возвращаем максимальный номер + 1
            return max_number + 1
        except Exception as e:
            return 1


    # метод используется когда нужно добавить новый отчёт.
    def add_new_report_entry(self, report_number, reg_number, report_date, last_change_date, owner_name, buyer_name, adress, valuation_cost="Оценка не окончена"):
        row_position = self.report_table.rowCount()
        self.report_table.insertRow(row_position)

        # Добавляем чекбокс в первую колонку
        checkbox = QTableWidgetItem()
        checkbox.setFlags(Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        checkbox.setCheckState(Qt.Unchecked)
        self.report_table.setItem(row_position, 0, checkbox)

        # Заполняем ячейки
        values = [report_number, reg_number, report_date, last_change_date, owner_name, buyer_name, adress, valuation_cost]
        for col_index, value in enumerate(values, start=1):
            self.report_table.setItem(row_position, col_index, QTableWidgetItem(str(value)))

        # Настраиваем отображение
       
        header = self.report_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)



    # Метод привязанный к кнопке
    def open_new_report(self):
        self.is_edit_mode = False  # Устанавливаем флаг на создание нового отчета
        self.new_report_window = NewReportWindow(self)
        self.new_report_window.setWindowModality(Qt.ApplicationModal)
        self.new_report_window.exec_()

       
    
    def find_report_row(self, report_number):
        for row in range(self.report_table.rowCount()):
            item = self.report_table.item(row, 1)  # 0 — столбец с номером отчета
            if item and item.text() == report_number:
                return row
        return None


    # метод для обновления существующего отчёта
    def update_report_entry(self, row, report_number, reg_number, report_date, last_change_date, owner_name, buyer_name, adress, valuation_cost="Оценка не окончена"):
        values = [report_number, reg_number, report_date, last_change_date, owner_name, buyer_name, adress, valuation_cost]
        for col_index, value in enumerate(values, start=1):
            self.report_table.setItem(row, col_index, QTableWidgetItem(str(value)))

        
        header = self.report_table.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.Stretch)




    def select_save_directory(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Выберите папку для сохранения отчётов", "")
        if folder_path:
            self.save_directory = folder_path
            self.save_settings()  # <--- сохраняем в settings.json
            QMessageBox.information(self, "Путь сохранён", f"Отчёты будут сохраняться в:\n{self.save_directory}")
        else:
            QMessageBox.warning(self, "Отмена", "Папка не выбрана.")


    def add_report_to_registry(self, report_number, reg_number, report_date, owner_name, buyer_name, adress, valuation_cost="Оценка не окончена"):
        try:
            # Добавляем отчёт в реестр
            self.report_registry.add_report(report_number, reg_number, report_date, owner_name, buyer_name, adress, valuation_cost="Оценка не окончена")
            
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось добавить отчёт в реестр: {str(e)}")

    # выгружаем данные из файла реестра для заполнения таблицы
    def load_reports_from_registry(self):
        try:
            # Проверяем наличие файла перед загрузкой
            registry_path = os.path.join(self.project_dir, "data", "report_registry.json")
            if not os.path.exists(registry_path):
                with open(registry_path, "w", encoding="utf-8") as file:
                    json.dump({"reports": []}, file, ensure_ascii=False, indent=4)

            # Загружаем данные из реестра
            with open(registry_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Очищаем таблицу перед загрузкой
            self.report_table.setRowCount(0)

            # Удаляем дубликаты на этапе загрузки
            loaded_reports = set()

            # Сортируем по дате регистрации
            sorted_reports = sorted(
                data.get("reports", []),
                key=lambda r: QDate.fromString(r.get("report_date", ""), "yyyy-MM-dd")
            )

        
           # Заполняем таблицу
            for report in sorted_reports:
                report_id = report.get("report_number")
                if report_id not in loaded_reports:
                    self.add_new_report_entry(
                        report.get("report_number", "Не указан"),
                        report.get("reg_number", "Не указан"),  # ← безопасно
                        report.get("report_date", "Не указана"),
                        report.get("last_change_date", "Не указана"),
                        report.get("owner_name", "Не указан"),
                        report.get("buyer_name", "Не указан"),
                        report.get("adress", "Не указан"),
                        report.get("valuation_cost", "Оценка не окончена")
                    )
                    loaded_reports.add(report_id)

        except Exception as e:
            print("")





    # открывает существующи отчёт кликом
    def open_report(self, item):
        # Получаем строку, по которой кликнули
        row = item.row()
        report_number = self.report_table.item(row, 1).text()  # Берём значение из первого столбца

        # Получаем данные из реестра
        registry_data = self.report_registry.get_report_data(report_number)

        # Получаем данные из файла отчёта через ReportFileManager
        report_data = self.report_manager.load_report_data(report_number)

        # Проверяем, удалось ли загрузить данные
        if registry_data:
            # Устанавливаем флаг на редактирование отчёта
            self.is_edit_mode = True

            # Открываем окно оценки с данными
            self.valuation_window = ValuationMainWindow(self, report_number)

            # Передаём данные из реестра (общая информация) и из файла (детальная информация)
            combined_data = {**registry_data, **report_data}  # Объединяем оба словаря
            self.valuation_window.load_data(combined_data)
            # Проверяем наличие вкладки "Затратный подход" (укрупнённая стоимость)
            if hasattr(self.valuation_window, 'ukup_tab') and hasattr(self.valuation_window.ukup_tab, 'load_liters_to_table'):
                # Загрузка литеров в таблицу
                liters = report_data.get("liters", [])
                self.valuation_window.ukup_tab.load_liters_to_table(self.valuation_window.saved_liters)

            else:
                print("Ошибка: вкладка 'Затратный подход' не инициализирована.")

            self.valuation_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", f"Отчёт №{report_number} не найден.")





    def get_report_data(self, report_number):
        try:
            with open(f"reports/report_{report_number}.json", "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception as e:
            return None
        

   
    def delete_selected_reports(self):
        rows_to_delete = []
        for row in range(self.report_table.rowCount()):
            checkbox_item = self.report_table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:
                rows_to_delete.append(row)

        if not rows_to_delete:
            QMessageBox.warning(self, "Удаление", "Не выбраны отчеты для удаления.")
            return

        for row in reversed(rows_to_delete):
            report_number = self.report_table.item(row, 1).text()
            reg_number = self.report_table.item(row, 2).text().strip()

            try:
                # Удаляем из реестра
                self.report_registry.remove_report(report_number)
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить отчёт из реестра: {str(e)}")
                continue

            # Удаляем строку из таблицы
            self.report_table.removeRow(row)

            # Удаляем папку с Ko'chirma, Kadastr, Word и т.д.
            try:
                report_folder = os.path.join(self.save_directory, reg_number)
                if os.path.exists(report_folder) and os.path.isdir(report_folder):
                    shutil.rmtree(report_folder)
                    print(f"[INFO] Папка отчёта {report_folder} успешно удалена.")
            except Exception as e:
                print(f"[ERROR] Не удалось удалить папку отчёта {report_number}: {e}")


        QMessageBox.information(self, "Удаление", "Выбранные отчеты и связанные файлы успешно удалены.")





    def copy_selected_reports(self):
        for row in range(self.report_table.rowCount()):
            checkbox_item = self.report_table.item(row, 0)
            if checkbox_item and checkbox_item.checkState() == Qt.Checked:

                # Получаем данные выбранного отчета
                report_number = self.report_table.item(row, 1).text()
                reg_number = "Дубликат"
                report_date = self.report_table.item(row, 3).text()
                last_change_date = QDate.currentDate().toString("yyyy-MM-dd")
                owner_name = self.report_table.item(row, 5).text()
                buyer_name = self.report_table.item(row, 6).text()
                adress = self.report_table.item(row, 7).text()
                valuation_cost = self.report_table.item(row, 8).text()

                # Получаем полный объект отчета
                original_report = self.get_report_data(report_number)

                new_report_number = str(self.get_last_report_number())


                # Создаем копию данных (не изменяя оригинал)
                report_copy = original_report.copy()
                report_copy[ValuationMainWindow.REPORT_FIELDS["number"]] = new_report_number
                report_copy[ValuationMainWindow.REPORT_FIELDS["reg_number"]] = "Дубликат" 
                report_copy["is_copy"] = True
                report_copy["original_number"] = report_number  # Сохраняем номер оригинала

                # Добавляем копию отчета в реестр и таблицу
                self.add_report_to_registry(new_report_number, reg_number, report_date, owner_name, buyer_name, adress, valuation_cost)
                self.add_new_report_entry(new_report_number, reg_number, report_date, last_change_date, owner_name, buyer_name, adress, valuation_cost)

                # Сохраняем копию на диск как новый файл
                self.report_manager.save_report_data(new_report_number, report_copy)

        QMessageBox.information(self, "Копирование", "Выбранные отчеты успешно скопированы.")
        for row in range(self.report_table.rowCount()):
            checkbox_item = self.report_table.item(row, 0)
            if checkbox_item:
                checkbox_item.setCheckState(Qt.Unchecked)


    
    
    @staticmethod
    def filter_report_data(data):
        # Маппинг ключей, которые нужны для таблицы и реестра
        field_map = {
            "report_number": "report_number",
            "reg_number": "reg_number",
            "report_date": "contract_date",
            "last_change_date": "inspection_date",
            "owner_name": "owner_name",
            "buyer_name": "buyer_name",
            "adress": "address",
            "valuation_cost": "valuation_cost"
        }

        filtered_data = {}
        for key, path in field_map.items():
            # Разделяем путь, если он вложенный
            keys = path.split(".")
            value = data
            try:
                for k in keys:
                    value = value.get(k, "Не указан")
                filtered_data[key] = value
            except Exception:
                filtered_data[key] = "Не указан"

        return filtered_data



    def update_report_in_table(self, new_report_number, data):
        # Ищем строку с номером отчета в таблице
        for row in range(self.report_table.rowCount()):
            current_number = self.report_table.item(row, 1).text()

            # Если найден старый номер или оригинальный номер копии
            if current_number == data.get("original_number", new_report_number) or current_number == new_report_number:
                # Обновляем строку с новыми данными
                report_date = data.get(self.valuation_window.REPORT_FIELDS["contract_date"], "Не указан")
                reg_number = data.get(self.valuation_window.REPORT_FIELDS['reg_number'], 'Не указан')
                last_change_date = QDate.currentDate().toString("yyyy-MM-dd")
                owner_name = data.get(self.valuation_window.REPORT_FIELDS["owner"], "Не указан")
                buyer_name = data.get(self.valuation_window.REPORT_FIELDS["buyer_name"], "Не указан")
                adress = data.get(self.valuation_window.REPORT_FIELDS["address"], "Не указан")
                valuation_cost = data.get(self.valuation_window.REPORT_FIELDS["valuation_cost"], "Оценка не окончена")

                # Обновляем данные в существующей строке
                self.update_report_entry(row, new_report_number, reg_number, report_date, last_change_date, owner_name, buyer_name, adress, valuation_cost)
                return

        # Если не найден, добавляем новую строку
        self.add_new_report_entry(new_report_number, 
                            data.get(self.valuation_window.REPORT_FIELDS['reg_number'], 'Не указан'),
                            data.get(self.valuation_window.REPORT_FIELDS["contract_date"], "Не указан"),
                            QDate.currentDate().toString("yyyy-MM-dd"),
                            data.get(ValuationMainWindow.REPORT_FIELDS["owner"], "Не указан"),
                            data.get(ValuationMainWindow.REPORT_FIELDS["buyer_name"], "Не указан"),
                            data.get(ValuationMainWindow.REPORT_FIELDS["address"], "Не указан"),
                            data.get(ValuationMainWindow.REPORT_FIELDS["valuation_cost"], "Оценка не окончена"))


        
        
    def save_settings(self):
        settings_path = os.path.join(self.project_dir, "settings.json")
        try:
            with open(settings_path, "w", encoding="utf-8") as f:
                json.dump({"save_directory": self.save_directory}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения настроек: {str(e)}")

    def load_settings(self):
        settings_path = os.path.join(self.project_dir, "settings.json")
        if os.path.exists(settings_path):
            try:
                with open(settings_path, "r", encoding="utf-8") as f:
                    settings = json.load(f)
                    self.save_directory = settings.get("save_directory", "")
            except Exception as e:
                print(f"Ошибка загрузки настроек: {str(e)}")
                self.save_directory = ""
        else:
            self.save_directory = ""



    