# from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QComboBox, QMessageBox, QLineEdit, QLabel
# from ui.pages.description_dialog import DescriptionDialog
# import pandas as pd

# class Page2Filtering(QWidget):
#     def __init__(self, widget, parent=None, service=None):
#         super().__init__(parent)
#         self.widget = widget
#         self.parent = parent
#         self.service = service

#         self.df_filtered = None
#         self.filtered_df_original = None

#         self.combo_mapping = {
#             "Этажность": "floor",
#             "Материал стен": "wall_material",
#             "Перекрытие": "overlap",
#             "Кровля": "roof",
#             "Фундаменты": "foundation",
#             "Полы": "flooring",
#             "Толщина стен": "wall_thickness",
#             "Высота": "wall_high",
#             "Примыкание": "wall_junction",
#             "Отделка": "decoration"
#         }

#         self.combo_boxes = {v: self.widget.findChild(QComboBox, v) for v in self.combo_mapping.values()}
#         for combo in self.combo_boxes.values():
#             combo.hide()

#         # Лейблы
#         self.qline_labels = {}
#         qlinelabel_names = ["label_square", "label_high", "label_weight", "label_length"]

#         for name in qlinelabel_names:
#             self.qline_labels[name] = self.widget.findChild(QLabel, name)

#         self.combo_labels = {}
#         combolabel_names = ["label_floor", "label_foundation", "label_flooring", "label_wall_material",
#                        "label_overlap", "label_roof", "label_wall_thickness", "label_wall_high", "label_wall_junction", "label_decoration"]

#         for name in combolabel_names:
#             self.combo_labels[name] = self.widget.findChild(QLabel, name)


#         # Кнопки
#         self.pushButton_choose_analog = self.widget.findChild(QPushButton, "pushButton_choose_analog")
#         self.pushButton_back_to_page_1 = self.widget.findChild(QPushButton, "pushButton_back_to_page_1")
#         self.pushButton_choose_analog.clicked.connect(self.choose_analog)
#         # self.pushButton_choose_analog.clicked.connect(self.collect_data)
#         self.pushButton_back_to_page_1.clicked.connect(self.back_and_reset)
        
#         #Таблица
#         self.filtered_table = self.widget.findChild(QTableWidget, "filtered_table")
#         self.filtered_table.setEditTriggers(QTableWidget.NoEditTriggers)
#         self.filtered_table.setSelectionBehavior(QTableWidget.SelectRows)
#         self.filtered_table.setSelectionMode(QTableWidget.SingleSelection)
#         self.filtered_table.cellDoubleClicked.connect(self.open_description_dialog)

#         # Поля для ввода
#         self.line_square = self.widget.findChild(QLineEdit, "square")
#         self.line_high = self.widget.findChild(QLineEdit, "high")
#         self.line_weight = self.widget.findChild(QLineEdit, "weight")
#         self.line_length = self.widget.findChild(QLineEdit, "length")
#         self.label_selected_building = self.widget.findChild(QLabel, "label_selected_building")

#         # Установка значений
#         self.line_square.textChanged.connect(self.handle_square_or_high_changed)
#         self.line_high.textChanged.connect(self.handle_square_or_high_changed)



#     def update_visible_fields(self):
#         df = self.df_filtered
#         # Скрываем элементы
#         self.line_square.hide()
#         self.line_high.hide()
#         self.line_weight.hide()
#         self.line_length.hide()

#         self.qline_labels["label_square"].hide()
#         self.qline_labels["label_high"].hide()
#         self.qline_labels["label_weight"].hide()
#         self.qline_labels["label_length"].hide()

#         # Если нет данных - не показываем
#         if df is None or df.empty:
#             return

#         # Логика показа

#         # 1. Проверяем "Объём до м3"
#         if df['Объём до м3'].notna().any():
#             # Если хотя0 бы один объём не NaN, показываем площадь, высоту и вес
#             self.line_square.show()
#             self.line_high.show()
#             self.line_weight.show()
#             self.qline_labels["label_square"].show()
#             self.qline_labels["label_high"].show()
#             self.qline_labels["label_weight"].show()

#         # 2. Проверяем наличие значения "Площадь до м2"
#         elif df['Площадь до м2'].notna().any():
#             # Показываем площадь в любом случае
#             self.line_square.show()
#             self.qline_labels["label_square"].show()

#             # Если хотя бы у одного аналога есть высота, показываем её
#             if df['Высота'].notna().any():
#                 self.line_high.show()
#                 self.qline_labels["label_high"].show()

#             # Дополнительное условие для типов зданий, которые требуют высоту по умолчанию
#             building_type = self.label_selected_building.text()
#             if building_type == "Жилой дом":
#                 # Для жилого дома высота всегда показывается
#                 self.line_high.show()
#                 self.qline_labels["label_high"].show()

#         # 3. Проверяем наличие значения "Протяженность"
#         elif df['Протяженность'].notna().any():
#             # Показываем длину
#             self.line_length.show()
#             self.qline_labels["label_length"].show()



#     def handle_square_or_high_changed(self):
#         self.calculate_weight()

#     def calculate_weight(self):
#         try:
#             square = float(self.line_square.text().replace(',', '.')) if self.line_square.isVisible() else 0
#             high = float(self.line_high.text().replace(',', '.')) if self.line_high.isVisible() else 0
#             weight = square * high
#             self.line_weight.setText(str(round(weight, 2)))
#         except ValueError:
#             self.line_weight.setText('0')


#     def show_filtered_table(self, df):
#         df_to_show = df.dropna(axis=1, how='all')
#         self.filtered_table.setRowCount(0)
#         self.filtered_table.setColumnCount(len(df_to_show.columns))
#         self.filtered_table.setHorizontalHeaderLabels(df_to_show.columns)
#         for row_idx, (_, row) in enumerate(df_to_show.iterrows()):
#             self.filtered_table.insertRow(row_idx)
#             for col_idx, value in enumerate(row):
#                 item = QTableWidgetItem(str(value) if pd.notna(value) else "")
#                 self.filtered_table.setItem(row_idx, col_idx, item)

#     def load_filtered_data(self, building_type):
#         self.reset_all_filters()
#         self.df_filtered = self.service.get_filtered_ukup(building_type).copy()
#         self.filtered_df_original = self.df_filtered.copy()
#         self.setup_initial_ui()
#         self.show_filtered_table(self.df_filtered)
#         self.label_selected_building.setText(building_type)
#         self.parent.selected_building_type = building_type
#         self.update_visible_fields()  # Добавить сюда!


#     def reset_all_filters(self):
#         for combo in self.combo_boxes.values():
#             combo.blockSignals(True)
#             combo.clear()
#             combo.hide()
#             combo.blockSignals(False)
#         for label in self.combo_labels.values():
#             label.hide()    
#         self.filtered_table.setRowCount(0)
#         self.df_filtered = None
#         self.filtered_df_original = None
#         self.line_square.clear()
#         self.line_high.clear()
#         self.line_weight.clear()
#         self.line_length.clear()

#     def back_and_reset(self):
#         """Назад на первую страницу без сброса данных при редактировании"""
#         # Проверяем, редактируем ли мы существующий отчет
#         if hasattr(self.parent, 'is_edit_mode') and self.parent.is_edit_mode:
#             self.parent.params_for_liter.setCurrentIndex(0)
#         else:
            
#             self.reset_all_filters()
#             self.parent.params_for_liter.setCurrentIndex(0)


#     def setup_initial_ui(self):
#         """Первый запуск - показать первый comboBox"""
#         self.df_filtered = self.filtered_df_original.copy()

#         for combo in self.combo_boxes.values():
#             combo.hide()
#             combo.clear()

#         # Показываем первый параметр (если есть выбор)
#         for column, combo_name in self.combo_mapping.items():
#             combo = self.combo_boxes[combo_name]
#             unique_vals = self.df_filtered[column].dropna().unique()

#             if len(unique_vals) == 0:
#                 combo.hide()
#             elif len(unique_vals) == 1:
#                 # Автоматически применяем
#                 self.df_filtered = self.df_filtered[self.df_filtered[column] == unique_vals[0]]
#                 combo.hide()
#             else:
#                 combo.show()
#                 label_name = "label_" + combo_name
#                 if label_name in self.combo_labels:
#                     self.combo_labels[label_name].show()
#                 combo.addItem("Выберите из списка")
#                 combo.addItems(map(str, unique_vals))
#                 combo.blockSignals(True)
#                 combo.setCurrentIndex(0)
#                 combo.blockSignals(False)
#                 combo.currentIndexChanged.connect(lambda _, col=column, name=combo_name: self.on_combo_changed(col, name))
#                 break  # Показали первый выбор, остальные пока скрыты
    
    
#     def on_combo_changed(self, column, combo_name):
#         """Фильтрация по combo и показ следующего comboBox"""
#         selected_value = self.combo_boxes[combo_name].currentText()
#         if selected_value == "Выберите из списка":
#             return  # Если ничего не выбрано

#         # =====================
#         # 1. Сбор всех фильтров
#         # =====================
#         applied_filters = {}
#         for col, name in self.combo_mapping.items():
#             combo = self.combo_boxes[name]
#             if combo.isVisible() and combo.currentText() != "Выберите из списка":
#                 applied_filters[col] = combo.currentText()
#             if col == column:
#                 break  # Только до текущего выбранного

#         # ================================
#         # 2. Применяем фильтры по порядку
#         # ================================
#         self.df_filtered = self.filtered_df_original.copy()  # Сбрасываем фильтр
#         for col, value in applied_filters.items():
#             col_dtype = self.df_filtered[col].dtype
#             # Приведение типов
#             if pd.api.types.is_numeric_dtype(col_dtype):
#                 try:
#                     value = float(value)
#                 except ValueError:
#                     continue  # Пропустить некорректные значения
#             # Фильтрация
#             self.df_filtered = self.df_filtered[self.df_filtered[col] == value]
#             if self.df_filtered.empty:
#                 QMessageBox.warning(self, "Ошибка", f"Нет данных для фильтра: {col} = {value}")
#                 return  # Прерываем если пусто

#         # ==================================
#         # 3. Показать таблицу и обновить поля
#         # ==================================
#         self.show_filtered_table(self.df_filtered)
#         self.update_visible_fields()

#         # ========================================
#         # 4. Скрываем все combo после текущего
#         # ========================================
#         columns = list(self.combo_mapping.keys())
#         index = columns.index(column)
#         for col in columns[index + 1:]:
#             combo = self.combo_boxes[self.combo_mapping[col]]
#             combo.blockSignals(True)
#             combo.clear()
#             combo.hide()
#             combo.blockSignals(False)

#         # ==================================================
#         # 5. Показываем следующий comboBox (если есть выбор)
#         # ==================================================
#         for col in columns[index + 1:]:
#             name = self.combo_mapping[col]
#             combo = self.combo_boxes[name]
#             unique_vals = self.df_filtered[col].dropna().unique()
#             if len(unique_vals) > 1:
#                 combo.blockSignals(True)
#                 combo.clear()
#                 combo.addItem("Выберите из списка")
#                 combo.addItems(map(str, unique_vals))
#                 combo.setCurrentIndex(0)
#                 combo.blockSignals(False)
#                 combo.show()
#                 # ✅ Показываем лейбл к combo
#                 label_name = "label_" + name  # Название метки совпадает с логикой
#                 if label_name in self.combo_labels:
#                     self.combo_labels[label_name].show()
#                 combo.currentIndexChanged.connect(lambda _, c=col, n=name: self.on_combo_changed(c, n))
#                 break  # Ожидаем выбора следующего фильтра

#         # ============================================
#         # 6. Фильтрация по объему или площади (при вводе)
#         # ============================================
#         target_volume = self.get_target_volume()
#         target_area = self.get_target_area()

#         if target_volume and self.df_filtered['Объём до м3'].notna().any():
#             self.apply_final_volume_area_filter(target_volume=target_volume)
#         elif target_area and self.df_filtered['Площадь до м2'].notna().any():
#             self.apply_final_volume_area_filter(target_area=target_area)
#         else:
#             self.show_filtered_table(self.df_filtered)



#     def choose_analog(self): 
#         selected_items = self.filtered_table.selectedItems()
        
#         if not selected_items:
#             QMessageBox.warning(self, "Предупреждение", "Сначала выберите аналог")
#             return  # ⛔ Останавливаем выполнение, не переходим дальше

#         # Проверяем, требуется ли ввод высоты
#         if self.qline_labels["label_high"].isVisible():
#             fact_high = self.line_high.text().strip()
            
#             if not fact_high or not fact_high.replace(',', '.').replace('.', '', 1).isdigit():
#                 QMessageBox.warning(self, "Ошибка", "Введите корректную высоту перед выбором аналога.")
#                 return  # ⛔ Останавливаем выполнение, не переходим дальше
        
#         row = selected_items[0].row()
#         analog_id = self.df_filtered.index[row]  # ID берём из индекса
#         data = self.df_filtered.loc[analog_id].to_dict()  # Преобразуем строку в словарь
        
#         # 🔥 Вызов метода collect_data для сбора актуальных данных
#         collected_data = self.collect_data()
       

#         # Сохраняем данные на второй странице в общий словарь liter_data
#         self.parent.liter_data["page2"] = collected_data
        
                
#         # Передача данных в Page3
#         self.pass_data_to_page3(data, analog_id)  # Передаем словарь с данными
#         self.set_description_in_page3(analog_id)  # Передаем описание

        
       
        
#         # Передача ID для загрузки конструктивных элементов
#         self.parent.page3.receive_building_data(analog_id)  # Загружаем элементы

        
#         self.parent.params_for_liter.setCurrentIndex(2)  # ✅ Переходим на Page3 только если все проверки пройдены

    
        





#     def open_description_dialog(self, row, column):
#         analog_id = self.df_filtered.index[row]
#         df_description = self.service.description()
        
#         if df_description is None or df_description.empty or analog_id not in df_description.index:
#             QMessageBox.warning(self, "Ошибка", "Нет данных для описания аналога.")
#             return
        
#         dialog = DescriptionDialog(analog_id, df_description, self)
#         dialog.exec_()

#     def get_row_data(self, row):
#         data = {}
#         if self.df_filtered is not None:
#             try:
#                 df_index = self.df_filtered.index[row]
#                 data['ID'] = df_index  # Возможно, ID находится в индексе
#             except IndexError:
#                 data['ID'] = None
#         for column in range(self.filtered_table.columnCount()):
#             header = self.filtered_table.horizontalHeaderItem(column).text()
#             item = self.filtered_table.item(row, column)
#             data[header] = item.text() if item else ''
        
#         return data

    

#     def apply_final_volume_area_filter(self, target_volume=None, target_area=None):
#         """Последняя фильтрация аналогов по объему или площади"""
#         if len(self.df_filtered) > 1:
#             if target_volume is not None and self.df_filtered['Объём до м3'].notna().any():
#                 df_sorted = self.df_filtered[self.df_filtered['Объём до м3'].notna()].sort_values('Объём до м3')
#                 for _, row in df_sorted.iterrows():
#                     if target_volume <= row['Объём до м3']:
#                         self.df_filtered = pd.DataFrame([row])
#                         break
#                 else:
#                     self.df_filtered = pd.DataFrame([df_sorted.iloc[-1]])

#             elif target_area is not None and self.df_filtered['Площадь до м2'].notna().any():
#                 df_sorted = self.df_filtered.sort_values('Площадь до м2')
#                 for _, row in df_sorted.iterrows():
#                     if target_area <= row['Площадь до м2']:
#                         self.df_filtered = pd.DataFrame([row])
#                         break
#                 else:
#                     self.df_filtered = pd.DataFrame([df_sorted.iloc[-1]])

#         # Обновляем таблицу
#         self.show_filtered_table(self.df_filtered)


#     def get_target_volume(self):
#         try:
#             return float(self.line_weight.text().replace(',', '.'))
#         except ValueError:
#             return None

#     def get_target_area(self):
#         try:
#             return float(self.line_square.text().replace(',', '.'))
#         except ValueError:
#             return None

#     def pass_data_to_page3(self, data, building_id):
#         """Передача данных из Page2 в Page3"""
#         price_per_m2 = data.get('Стоимость', 'Нет данных')  # Теперь data - это словарь
#         self.parent.page3.label_price_per_m2.setText(f"Стоимость за м² по УКУП: {price_per_m2}")
#         fact_high = self.line_high.text()
#         self.parent.page3.set_fact_high(fact_high, building_id=building_id)





#     def get_selected_price_per_m2(self):
#         """Получает стоимость за м² из отфильтрованных данных"""
#         if self.df_filtered is not None and not self.df_filtered.empty:
#             price_column = "Стоимость"
#             if price_column in self.df_filtered.columns:
#                 return str(self.df_filtered[price_column].values[0])
#         return "Нет данных"
   
#     def go_to_analog_page(self):
#         """Переход на Page3 и передача данных"""
#         self.pass_data_to_page3()
#         self.parent.params_for_liter.setCurrentIndex(2)
   
   
#     def set_description_in_page3(self, analog_id):
#         """Передача описания аналога в Page3 с автоматическим масштабированием"""
#         df_description = self.service.description()
        
#         if df_description is None:
          
#             QMessageBox.warning(self, "Ошибка", "Не удалось загрузить описание аналогов.")
#             return

#         # ✅ Преобразуем ID в int, если он строковый
#         try:
#             analog_id = int(analog_id)
#         except ValueError:
#             QMessageBox.warning(self, "Ошибка", f"Некорректный ID аналога: {analog_id}")
#             return

#         # ✅ Проверяем, есть ли ID в индексе
#         if analog_id not in df_description.index:
           
#             QMessageBox.warning(self, "Ошибка", f"Нет описания для ID: {analog_id}")
#             return
        
#         # ✅ Извлекаем данные по ID
#         df_filtered = df_description.loc[[analog_id]]
        

        

#         for row in range(df_filtered.shape[0]):
#             for col in range(df_filtered.shape[1]):
#                 value = df_filtered.iat[row, col]
#                 item = QTableWidgetItem(str(value))
#                 # self.parent.page3.tableWidget_description.setItem(row, col, item)

#         # ✅ Автоматическое масштабирование столбцов
#         # self.parent.page3.tableWidget_description.horizontalHeader().setStretchLastSection(True)  
#         # self.parent.page3.tableWidget_description.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
   
#     def get_data(self):
#         """Собирает данные со второй страницы (Page2)"""

#         # Собираем данные из комбобоксов
#         combo_data = {}
#         for key, combo in self.combo_boxes.items():
#             if combo.isVisible():
#                 selected_value = combo.currentText()
#                 combo_data[key] = selected_value

#         # Собираем данные из текстовых полей
#         line_data = {
#             "square": self.line_square.text(),
#             "high": self.line_high.text(),
#             "weight": self.line_weight.text(),
#             "length": self.line_length.text()
#         }

#         # Собираем выбранные элементы из таблицы
#         selected_items = []
#         for row in range(self.filtered_table.rowCount()):
#             if self.filtered_table.item(row, 0) and self.filtered_table.item(row, 0).isSelected():
#                 row_data = {}
#                 for col in range(self.filtered_table.columnCount()):
#                     header = self.filtered_table.horizontalHeaderItem(col).text()
#                     item = self.filtered_table.item(row, col)
#                     row_data[header] = item.text() if item else ""
#                 selected_items.append(row_data)

#         # Собираем текст из метки выбранного здания
#         selected_building = self.label_selected_building.text()

#         return {
#             "selected_building": selected_building,
#             "combo_data": combo_data,
#             "line_data": line_data,
#             "selected_items": selected_items
#         }

#     def collect_data(self):
#         """Собирает данные со второй страницы (Page2)"""

#         # Собираем данные из комбобоксов
#         combo_data = {}
#         for key, combo in self.combo_boxes.items():
#             if combo.isVisible():
#                 selected_value = combo.currentText()
#                 if selected_value != "Выберите из списка":
#                     combo_data[key] = selected_value

#         # Собираем данные из текстовых полей
#         line_data = {
#             "square": self.line_square.text().strip(),
#             "high": self.line_high.text().strip(),
#             "weight": self.line_weight.text().strip(),
#             "length": self.line_length.text().strip()
#         }

#         # Собираем выбранные элементы из таблицы
#         selected_items = []
#         selected_ranges = self.filtered_table.selectedRanges()
#         if selected_ranges:
#             row = selected_ranges[0].topRow()
#             row_data = {}
#             for col in range(self.filtered_table.columnCount()):
#                 header = self.filtered_table.horizontalHeaderItem(col).text()
#                 item = self.filtered_table.item(row, col)
#                 row_data[header] = item.text() if item else ""
#             selected_items.append(row_data)

#         # Собираем текст из метки выбранного здания
#         selected_building = self.label_selected_building.text()

#         collected_data = {
#             "selected_building": selected_building,
#             "combo_data": combo_data,
#             "line_data": line_data,
#             "selected_items": selected_items
#         }


#         return collected_data

        
#     def load_data(self, data):
#         """Загружает данные на вторую страницу (Page2)"""
#         try:
#             # Загружаем текстовые поля
#             line_data = data.get("line_data", {})
#             self.line_square.setText(line_data.get("square", ""))
#             self.line_high.setText(line_data.get("high", ""))
#             self.line_weight.setText(line_data.get("weight", ""))
#             self.line_length.setText(line_data.get("length", ""))

#             # Загружаем комбобоксы
#             combo_data = data.get("combo_data", {})
#             for key, combo in self.combo_boxes.items():
#                 value = combo_data.get(key, "Выберите из списка")
#                 if value:
#                     index = combo.findText(value)
#                     if index != -1:
#                         combo.setCurrentIndex(index)

#             # Загружаем выбранные элементы из таблицы
#             selected_items = data.get("selected_items", [])
#             if selected_items:
#                 self.filtered_table.setRowCount(len(selected_items))
#                 for row, item in enumerate(selected_items):
#                     for col, (header, value) in enumerate(item.items()):
#                         table_item = QTableWidgetItem(str(value))
#                         self.filtered_table.setItem(row, col, table_item)

#             # Загружаем текст метки выбранного здания
#             selected_building = data.get("selected_building", "Не указано")
#             self.label_selected_building.setText(selected_building)

          

#         except Exception as e:
           
#             QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные на вторую страницу: {str(e)}")

        