# from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QDoubleSpinBox, QComboBox, QHBoxLayout, QMessageBox, QPushButton
# from PyQt5.QtCore import Qt
# from logic.koefs_logic import KoefsService
# from logic.data_entry import DataEntryForm
# import os
# import json
# from logic.calculations import calculate_profit, get_unit_multiplier, get_actual_unit_value


# class Page4Final(QWidget):
#     def __init__(self, widget, parent=None, main_window=None, valuation_window=None, service=None, ukup_widget=None):
#         super().__init__(parent)
#         self.widget = widget  # Это page_4
#         self.parent = parent
#         self.service = service
#         self.main_window = main_window
#         self.valuation_window = valuation_window  # <-- добавлено

#         self.ukup_widget = ukup_widget


#         self.data_service = DataEntryForm()
#         self.koefs_service = KoefsService()

#         # Используем уже существующий layout из .ui
#         self.layout = self.widget.layout()

#         self.table = self.widget.findChild(QTableWidget, "tableWidget_replacement_cost")
#         self.table_wear_calculation = self.widget.findChild(QTableWidget, "tableWidget_wear_calculation")
#         self.table_wear_calculation.keyPressEvent = self.handle_key_press
#         self.pushButton_save_liter_cost = self.widget.findChild(QPushButton, "pushButton_save_liter_cost")
          
#         if self.pushButton_save_liter_cost:
#             self.pushButton_save_liter_cost.clicked.connect(self.save_liter_to_table)  
            


#         self.tableWidget_valuation_cost = self.widget.findChild(QTableWidget, "tableWidget_valuation_cost")
#         from PyQt5.QtWidgets import QHeaderView

#         # Настройка ширины столбцов при инициализации таблицы
#         self.tableWidget_valuation_cost.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
#         self.tableWidget_valuation_cost.horizontalHeader().setStretchLastSection(True)
#         self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
#         self.table.horizontalHeader().setStretchLastSection(True)
#         self.table_wear_calculation.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
#         self.table_wear_calculation.horizontalHeader().setStretchLastSection(True)
        

#         headers = [
#             "Стоимость по УКУП", "Ед. изм.", "Тип здания",  # ← переименовано
#             "Коэфф. СМР 2004-2025", "Коэфф. до 2004",        # ← переименовано
#             "Строит. затраты", "Прибыль предпринимателя %", "Восст. стоим. с ПП"
#         ]
#         self.table.setColumnCount(len(headers))
#         self.table.setHorizontalHeaderLabels(headers)

#         headers_final_table = [
#             "Восст. стоим", "Поправка к удельным весам", "Совокупный износ %",
#             "Совокупный износ (сум)", "Оценочная стоимость"]

#         self.tableWidget_valuation_cost.setColumnCount(len(headers_final_table))
#         self.tableWidget_valuation_cost.setHorizontalHeaderLabels(headers_final_table)

#         self.pushButton_back_to_page_3 = self.widget.findChild(QPushButton, "pushButton_back_to_page3")
#         if self.pushButton_back_to_page_3:
#             self.pushButton_back_to_page_3.clicked.connect(self.go_to_page3)
#         self.update_total_row()
#         self.populate_table()
        
        



#     def go_to_page3(self):
#         self.parent.params_for_liter.setCurrentIndex(2)
 
#     def populate_table(self):
#         try:
#             price_str = self.parent.page3.groupBox__final_price.title()
#             price_value = float(price_str.replace("Итоговая стоимость:", "").replace("сум", "").replace(" ", "").replace(",", "."))
#         except Exception as e:
#             price_value = 0.0

#         df_filtered = self.parent.page2.df_filtered
#         unit = get_actual_unit_value(df_filtered, self.parent.page2)

#         oblast = self.valuation_window.comboBox_oblast.currentText()
#         rayon = self.valuation_window.comboBox_rayon.currentText()

#         df_stat, df_reg = self.koefs_service.get_filtered_stat_and_regional(oblast, rayon)

#         try:
#             coeff_smr = df_stat['Коэфф'].prod()
#             coeff_smr = round(coeff_smr, 0)
#         except:
#             coeff_smr = 1.0

#         try:
#             self.coeff_combo = QComboBox()
#             self.coeff_mapping = {row['type']: row['coff'] for _, row in df_reg.iterrows()}
#             for type_name in self.coeff_mapping.keys():
#                 self.coeff_combo.addItem(type_name)
#             self.coeff_combo.currentIndexChanged.connect(self.update_coeff_91_04)
#             self.table.setCellWidget(0, 2, self.coeff_combo)
#             selected_type = self.coeff_combo.currentText()
#             regional_coeff = float(self.coeff_mapping[selected_type])
#         except:
#             regional_coeff = 1.0

#         build_cost = price_value * unit * regional_coeff * coeff_smr

#         # F = 0.26
#         # G = self.advance_input.value() / 100 if hasattr(self, 'advance_input') else 0.2
#         # H = self.years_input.value() if hasattr(self, 'years_input') else 1.5
#         profit_percent = 22

#         final_cost = build_cost + profit_percent / 100 * build_cost
#         self.final_cost = final_cost

#         self.table.setRowCount(1)

#         # Список не редактируемых столбцов
#         non_editable_columns = [0, 1, 3, 4, 5, 6, 7]

#         # Устанавливаем значения в ячейки с проверкой редактируемости
#         items = [
#             (0, f"{price_value:.2f}"),
#             (1, f"{unit}"),
#             (3, f"{coeff_smr}"),
#             (4, f"{regional_coeff:.2f}"),
#             (5, f"{build_cost:.2f}"),
#             (6, f"{profit_percent:.2f} %"),
#             (7, f"{final_cost:.2f}")
#         ]

#         for col, value in items:
#             item = QTableWidgetItem(value)
#             if col in non_editable_columns:
#                 item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Делаем ячейку не редактируемой
#             self.table.setItem(0, col, item)

#         # Добавляем интерактивные виджеты в нужные столбцы
#         # self.advance_input = QDoubleSpinBox()
#         # self.advance_input.setRange(15.0, 50.0)
#         # self.advance_input.setValue(20.0)
#         # self.advance_input.setSuffix(" %")
#         # self.advance_input.valueChanged.connect(self.update_profit)
#         # self.table.setCellWidget(0, 7, self.advance_input)

#         # self.years_input = QDoubleSpinBox()
#         # self.years_input.setRange(1.0, 2.5)
#         # self.years_input.setValue(1.5)
#         # self.years_input.setSuffix(" лет")
#         # self.years_input.setSingleStep(0.1)
#         # self.years_input.valueChanged.connect(self.update_profit)
#         # self.table.setCellWidget(0, 8, self.years_input)

#         # self.update_profit()
#         self.populate_final_table()




#     def update_coeff_91_04(self):
#         try:
#             selected_type = self.coeff_combo.currentText()
#             regional_coeff = float(self.coeff_mapping[selected_type])
#             self.table.setItem(0, 4, QTableWidgetItem(f"{regional_coeff}"))
#             self.update_profit()
#         except Exception as e:
#             QMessageBox.warning(self, "Ошибка обновления коэффициента", str(e))
        


#     def update_coeff_91_04(self):
#         try:
#             selected_type = self.coeff_combo.currentText()
#             regional_coeff = float(self.coeff_mapping[selected_type])
#             self.table.setItem(0, 4, QTableWidgetItem(f"{regional_coeff:.2f}"))  # ⬅️ Обновляем Коэфф. до 2004

#             # Пересчитываем build_cost
#             price_value = float(self.table.item(0, 0).text())
#             unit = float(self.table.item(0, 1).text())
#             coeff_smr = float(self.table.item(0, 3).text())

#             build_cost = price_value * unit * regional_coeff * coeff_smr
#             self.table.setItem(0, 5, QTableWidgetItem(f"{build_cost:.2f}"))

#             self.update_profit()
#         except Exception as e:
#             QMessageBox.warning(self, "Ошибка обновления коэффициента", str(e))

#     def update_profit(self):
#         try:
#             F = 0.26
#             G = self.advance_input.value() / 100
#             H = self.years_input.value()
#             profit_percent = calculate_profit(F, G, H)

#             # Отображаем процент с двумя знаками после запятой и символом "%"
#             self.table.setItem(0, 9, QTableWidgetItem(f"{profit_percent:.2f} %"))
            
#             build_cost = float(self.table.item(0, 5).text())
#             final = build_cost + profit_percent / 100 * build_cost  # Учтём, что profit_percent уже в процентах
#             self.table.setItem(0, 10, QTableWidgetItem(f"{final:.2f}"))
#         except Exception as e:
#             QMessageBox.warning(self, "Ошибка расчёта", str(e))
#         self.populate_final_table()

#     def load_structural_elements(self, building_id):
#         print(f"Загрузка конструктивных элементов для ID: {building_id}")
#         df = self.parent.data_service.structural_elements()
#         if df is None or df.empty:
#             QMessageBox.warning(self.parent, "Ошибка", "Нет данных по конструктивным элементам.")
#             return

#         if building_id not in df.index:
#             QMessageBox.warning(self.parent, "Ошибка", f"Нет данных для ID: {building_id}")
#             return

#         df_filtered = df.loc[[building_id], ["Конструкции", "Доля %"]].copy()
#         df_filtered["Поправка к удельным весам %"] = 0.0
#         df_filtered["Физический износ %"] = 0.0

#         self.populate_wear_table(df_filtered)
    
#     def populate_wear_table(self, df):
#         row_count = len(df) + 1
#         col_count = len(df.columns)
#         self.table_wear_calculation.setRowCount(row_count)
#         self.table_wear_calculation.setColumnCount(col_count)
#         self.table_wear_calculation.setHorizontalHeaderLabels(df.columns)

#         for row_idx, row in enumerate(df.itertuples(index=False)):
#             for col_idx, value in enumerate(row):
#                 item = QTableWidgetItem(str(value))
#                 if col_idx in [2, 3]:  # Колонки с редактируемыми значениями
#                     # Если значение пустое или не число, инициализируем как 0.0
#                     if not value or not str(value).replace('.', '', 1).isdigit():
#                         value = 0.0
#                     item = QTableWidgetItem(str(value))
#                     item.setFlags(item.flags() | Qt.ItemIsEditable)
#                 else:
#                     item.setFlags(item.flags() & ~Qt.ItemIsEditable)
#                 self.table_wear_calculation.setItem(row_idx, col_idx, item)

#         self.add_total_row(df)
#         self.table_wear_calculation.itemChanged.connect(self.update_total_row)
#         self.update_total_row()

#     def add_total_row(self, df):
#         row_idx = self.table_wear_calculation.rowCount() - 1
#         total_item = QTableWidgetItem("ВСЕГО")
#         total_item.setFlags(total_item.flags() & ~Qt.ItemIsEditable)
#         self.table_wear_calculation.setItem(row_idx, 0, total_item)
#         self.update_total_row()


#     def update_total_row(self):
#         row_idx = self.table_wear_calculation.rowCount() - 1
#         total_share = 0
#         total_adjustment = 0
#         weighted_wear_sum = 0

#         for row in range(row_idx):
#             try:
#                 share = self.table_wear_calculation.item(row, 1)
#                 adjustment = self.table_wear_calculation.item(row, 2)
#                 wear = self.table_wear_calculation.item(row, 3)

#                 # Получаем значения ячеек
#                 share_value = float(share.text()) if share and share.text() else 0.0
#                 adjustment_value = float(adjustment.text()) if adjustment and adjustment.text() else 0.0
#                 wear_value = float(wear.text()) if wear and wear.text() else 0.0
                
#                 # Накопление общей доли и поправки
#                 total_share += share_value
#                 total_adjustment += adjustment_value
                
#                 # Усреднённый физический износ (сумма взвешенных значений)
#                 weighted_wear_sum += (wear_value * share_value) / 100
#             except (ValueError, AttributeError):
#                 continue

#         avg_wear = weighted_wear_sum  # Средний износ уже учтён через взвешенные значения

#         self.total_adjustment = total_adjustment
#         self.avg_wear = avg_wear
#         self.table_wear_calculation.blockSignals(True)

#         # Установка значений в последнюю строку
#         self.table_wear_calculation.setItem(row_idx, 1, QTableWidgetItem(str(round(total_share, 2))))
#         self.table_wear_calculation.setItem(row_idx, 2, QTableWidgetItem(str(round(total_adjustment, 2))))
#         self.table_wear_calculation.setItem(row_idx, 3, QTableWidgetItem(str(round(avg_wear, 2))))

#         # Отключаем редактирование итоговой строки
#         for col in range(self.table_wear_calculation.columnCount()):
#             item = self.table_wear_calculation.item(row_idx, col)
#             if item:
#                 item.setFlags(item.flags() & ~Qt.ItemIsEditable)

#         self.table_wear_calculation.blockSignals(False)
#         self.populate_final_table()


#     def receive_building_data(self, building_id):
#         """Получает building_id от Page3 и загружает таблицу конструктивных элементов."""
#         self.building_id = building_id
#         self.load_structural_elements(self.building_id)
    
    
#     def handle_key_press(self, event):
#         """Обрабатывает нажатие клавиши Enter и стрелок для перемещения по ячейкам."""
#         current_row = self.table_wear_calculation.currentRow()
#         current_column = self.table_wear_calculation.currentColumn()

#         if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
#             # Переход вниз на одну строку
#             next_row = current_row + 1
#             if next_row < self.table_wear_calculation.rowCount():
#                 self.table_wear_calculation.setCurrentCell(next_row, current_column)
#                 self.table_wear_calculation.editItem(self.table_wear_calculation.item(next_row, current_column))
#         elif event.key() == Qt.Key_Up:
#             # Переход на строку выше
#             prev_row = max(0, current_row - 1)
#             self.table_wear_calculation.setCurrentCell(prev_row, current_column)
#             self.table_wear_calculation.editItem(self.table_wear_calculation.item(prev_row, current_column))
#         elif event.key() == Qt.Key_Down:
#             # Переход на строку ниже
#             next_row = min(self.table_wear_calculation.rowCount() - 1, current_row + 1)
#             self.table_wear_calculation.setCurrentCell(next_row, current_column)
#             self.table_wear_calculation.editItem(self.table_wear_calculation.item(next_row, current_column))
#         elif event.key() == Qt.Key_Left:
#             # Переход влево
#             prev_col = max(0, current_column - 1)
#             self.table_wear_calculation.setCurrentCell(current_row, prev_col)
#             self.table_wear_calculation.editItem(self.table_wear_calculation.item(current_row, prev_col))
#         elif event.key() == Qt.Key_Right:
#             # Переход вправо
#             next_col = min(self.table_wear_calculation.columnCount() - 1, current_column + 1)
#             self.table_wear_calculation.setCurrentCell(current_row, next_col)
#             self.table_wear_calculation.editItem(self.table_wear_calculation.item(current_row, next_col))
#         else:
#             # Стандартное поведение для редактирования
#             QWidget.keyPressEvent(self.table_wear_calculation, event)
    
    
    
    
    
#     def populate_final_table(self):
#         """Заполняет итоговую таблицу на основе данных из предыдущих расчетов."""
#         final_cost = getattr(self, "final_cost", 0.0)
#         total_adjustment = getattr(self, "total_adjustment", 0.0)
#         avg_wear = getattr(self, "avg_wear", 0.0)

#         self.tableWidget_valuation_cost.setRowCount(1)
#         final_adjustment = (100-total_adjustment)/100
#         final_wear = final_cost * avg_wear / 100
#         valuated_cost = final_cost*final_adjustment - (final_cost*final_adjustment) * (avg_wear / 100)
#         self.final_adjustment = final_adjustment
#         self.final_wear = final_wear
#         self.valuated_cost = valuated_cost
#         # Список значений для итоговой таблицы
#         items = [
#             (0, f"{final_cost:.2f}"),
#             (1, f" {final_adjustment:.2f}"),
#             (2, f"{avg_wear:.2f} %"),
#             (3, f"{final_wear:.2f}"),
#             (4, f"{valuated_cost:.2f}")
#         ]

#         # Заполнение таблицы и установка флага "не редактируемо"
#         for col, value in items:
#             item = QTableWidgetItem(value)
#             item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Делаем ячейку не редактируемой
#             self.tableWidget_valuation_cost.setItem(0, col, item)



#     def save_liter_to_table(self):
#         """Сохраняет данные литера в общую таблицу."""
#         if not self.valuation_window.saved_liters:
#             report_number = self.valuation_window.report_number_input.text()
#             file_path = os.path.join(self.valuation_window.main_window.project_dir, "reports", f"report_{report_number}.json")
#             if os.path.exists(file_path):
#                 with open(file_path, "r", encoding="utf-8") as f:
#                     existing_data = json.load(f)
#                     self.valuation_window.saved_liters = existing_data.get("liters", [])

#         page4_data = self.collect_page4_data()
#         self.parent.liter_data["page4"] = page4_data

#         building_type = getattr(self.parent, "selected_building_type", "Неизвестно")
#         final_cost = getattr(self, "final_cost", 0.0)
#         final_wear = getattr(self, "avg_wear", 0.0)
#         valuated_cost = final_cost - final_cost * final_wear / 100

#         if getattr(self.parent, "is_edit_mode", False):
#             liter_id = self.parent.liter_data.get("liter_id")
#             self.valuation_window.saved_liters = [
#                 liter for liter in self.valuation_window.saved_liters
#                 if liter.get("liter_id") != liter_id
#             ]
#         else:
#             liter_id = len(self.valuation_window.saved_liters) + 1

#         self.parent.liter_data["liter_id"] = liter_id
#         building_id = getattr(self, "building_id", None)
#         if building_id:
#             self.parent.liter_data["building_id"] = building_id

#         liter_full_data = {
#             "liter_id": liter_id,
#             "building_type": building_type,
#             "final_cost": final_cost,
#             "final_wear": final_wear,
#             "valuated_cost": valuated_cost,
#             "page1": self.parent.liter_data.get("page1", {}),
#             "page2": self.parent.liter_data.get("page2", {}),
#             "page3": self.parent.liter_data.get("page3", {}),
#             "page4": self.parent.liter_data.get("page4", {})
#         }
#         if not liter_id or not building_type:
#             QMessageBox.warning(self, "Ошибка", "Невозможно сохранить литер: отсутствует ID или тип здания.")
#             return
#         self.valuation_window.saved_liters.append(liter_full_data)

#         # Сохраняем весь отчёт
#         if hasattr(self.valuation_window, "collect_general_info"):
#             report_number = self.valuation_window.report_number_input.text()
#             full_data = self.valuation_window.collect_general_info()
#             full_data["liters"] = self.valuation_window.saved_liters

#             self.valuation_window.main_window.report_manager.save_report_data(report_number, full_data)

#         # 💡 Обновляем таблицу
#         self.valuation_window.ukup_tab.load_liters_to_table(self.valuation_window.saved_liters)

#         self.parent.save_liters_to_file()

#         self.parent.accept()


#     def collect_page4_data(self):
#         """Собирает данные с четвертой страницы (Page4Final)."""

#         # Данные из таблицы tableWidget_replacement_cost
#         replacement_cost_data = []
#         for row in range(self.table.rowCount()):
#             row_data = {}
#             for col in range(self.table.columnCount()):
#                 header = self.table.horizontalHeaderItem(col).text()
#                 item = self.table.item(row, col)
#                 row_data[header] = item.text() if item else ""
#             replacement_cost_data.append(row_data)

#         # Данные из таблицы tableWidget_wear_calculation
#         wear_calculation_data = []
#         for row in range(self.table_wear_calculation.rowCount()):
#             row_data = {}
#             for col in range(self.table_wear_calculation.columnCount()):
#                 header = self.table_wear_calculation.horizontalHeaderItem(col).text()
#                 item = self.table_wear_calculation.item(row, col)
#                 row_data[header] = item.text() if item else ""
#             wear_calculation_data.append(row_data)

#         # Данные из таблицы tableWidget_valuation_cost
#         valuation_cost_data = []
#         for row in range(self.tableWidget_valuation_cost.rowCount()):
#             row_data = {}
#             for col in range(self.tableWidget_valuation_cost.columnCount()):
#                 header = self.tableWidget_valuation_cost.horizontalHeaderItem(col).text()
#                 item = self.tableWidget_valuation_cost.item(row, col)
#                 row_data[header] = item.text() if item else ""
#             valuation_cost_data.append(row_data)

#         # Собранные данные в словаре
#         collected_data = {
#             "replacement_cost_data": replacement_cost_data,
#             "wear_calculation_data": wear_calculation_data,
#             "valuation_cost_data": valuation_cost_data
#         }

#         # print("Собранные данные с четвертой страницы (Page4Final):", collected_data)
#         return collected_data


#     def load_data(self, data):
#         """Загружает данные на четвертую страницу (Page4Final)"""
#         try:
#             # Загрузка данных из таблицы replacement_cost_data
#             replacement_cost_data = data.get("replacement_cost_data", [])
#             self.table.setRowCount(len(replacement_cost_data))
#             for row, row_data in enumerate(replacement_cost_data):
#                 for col, (header, value) in enumerate(row_data.items()):
#                     item = QTableWidgetItem(str(value))
#                     if col in [7, 8]:  # Колонки с интерактивными элементами
#                         if col == 7:  # Аванс. платежи
#                             spinbox = QDoubleSpinBox()
#                             spinbox.setRange(15.0, 50.0)
#                             spinbox.setValue(float(value.replace(" %", "")) if value else 20.0)
#                             spinbox.setSuffix(" %")
#                             spinbox.valueChanged.connect(self.update_profit)
#                             self.table.setCellWidget(row, col, spinbox)
#                         elif col == 8:  # Лет стр-ва
#                             spinbox = QDoubleSpinBox()
#                             spinbox.setRange(1.0, 2.5)
#                             spinbox.setValue(float(value.replace(" лет", "")) if value else 1.5)
#                             spinbox.setSuffix(" лет")
#                             spinbox.setSingleStep(0.1)
#                             spinbox.valueChanged.connect(self.update_profit)
#                             self.table.setCellWidget(row, col, spinbox)
#                     else:
#                         self.table.setItem(row, col, item)

#             # Загрузка данных из таблицы wear_calculation_data
#             wear_calculation_data = data.get("wear_calculation_data", [])
#             self.table_wear_calculation.setRowCount(len(wear_calculation_data))
#             for row, row_data in enumerate(wear_calculation_data):
#                 for col, (header, value) in enumerate(row_data.items()):
#                     item = QTableWidgetItem(str(value))
#                     self.table_wear_calculation.setItem(row, col, item)

#             # Загрузка данных из таблицы valuation_cost_data
#             valuation_cost_data = data.get("valuation_cost_data", [])
#             self.tableWidget_valuation_cost.setRowCount(len(valuation_cost_data))
#             for row, row_data in enumerate(valuation_cost_data):
#                 for col, (header, value) in enumerate(row_data.items()):
#                     item = QTableWidgetItem(str(value))
#                     self.tableWidget_valuation_cost.setItem(row, col, item)

#             # Пересчет итоговых значений
#             self.update_profit()

#             # print(f"Page4Final: Данные успешно загружены: {data}")

#         except Exception as e:
#             # print(f"Ошибка при загрузке данных на четвертой странице (Page4Final): {str(e)}")
#             QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные на четвертую страницу: {str(e)}")


#     def load_liters_from_file(self, file_path):
#         """Загружает данные литера из файла в таблицу (ТОЛЬКО В ТАБЛИЦУ НА УКУП)"""
#         import json

#         try:
#             with open(file_path, 'r', encoding='utf-8') as file:
#                 data = json.load(file)

#             liters = data.get("liters", [])

#             # Получаем ссылку на таблицу литеров
#             liter_table = self.main_window.ukup_tab.tableWidget_liter_list

#             # Заполняем таблицу литеров
#             liter_table.setRowCount(len(liters))
#             for row, liter in enumerate(liters):
#                 liter_id = liter.get("liter_id", "")
#                 building_type = liter.get("building_type", "Неизвестно")
#                 final_cost = liter.get("final_cost", 0.0)
#                 final_wear = liter.get("final_wear", 0.0)
#                 valuated_cost = liter.get("valuated_cost", 0.0)

#                 items = [
#                     (0, str(liter_id)),  # Номер литера
#                     (1, building_type),  # Здание
#                     (2, f"{final_cost:,.2f}".replace(",", " ")),  # Восст. стоимость
#                     (3, f"{final_wear:.2f} %"),  # Усреднённый износ
#                     (4, f"{valuated_cost:,.2f}".replace(",", " "))  # Оценочная стоимость
#                 ]

#                 for col, value in items:
#                     item = QTableWidgetItem(value)
#                     item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Делаем ячейку не редактируемой
#                     liter_table.setItem(row, col, item)

#         except Exception as e:
#             print(f"Ошибка при загрузке литеров из файла: {str(e)}")
