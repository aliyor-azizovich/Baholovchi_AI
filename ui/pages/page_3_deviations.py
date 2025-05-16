# from PyQt5.QtWidgets import QWidget, QPushButton, QTableWidget, QComboBox, QGroupBox, QTableWidgetItem, QVBoxLayout, QMessageBox, QLineEdit, QLabel,QCheckBox, QHeaderView
# import pandas as pd
# from PyQt5.QtCore import Qt


# class page_3_deviations(QWidget):
#     def __init__(self, widget, parent=None, service=None, main_window=None, valuation_window=None):
#         super().__init__(parent)
#         self.widget = widget
#         self.parent = parent
#         self.service = service
#         self.main_window = main_window
#         self.building_id = getattr(parent, "building_id", None)  # Получаем ID из родителя
#         self.valuation_window = valuation_window  # <-- добавляем



#         self.facade_data = self.parent.data_service.facade()  
#         self.altitude_data = self.parent.data_service.altitude()

#         self.building_id = None

#     #    Промежуточные переменные для хранения откорректированной стоимости
#         self.facade_corrected_price = None
#         self.altitude_corrected_price = None
        
     
       

                 

#         # Элементы UX
#         self.groupBox_facade = self.widget.findChild(QGroupBox, "groupBox_facade")
#         self.comboBox_facade = self.widget.findChild(QComboBox, "comboBox_facade")
#         self.label_facade_result = self.widget.findChild(QLabel, "label_facade_result")
#         self.groupBox_high_correct = self.widget.findChild(QGroupBox, "groupBox_high_correct")
#         self.label_high_correction = self.widget.findChild(QLabel, "label_high_correction")
#         self.label_fact_high = self.widget.findChild(QLabel, "label_fact_high")
#         self.label_correction = self.widget.findChild(QLabel, "label_correction")
#         self.label_high_result = self.widget.findChild(QLabel, "label_high_result")
#         self.groupBox__final_price = self.widget.findChild(QGroupBox, "groupBox__final_price")
#         self.pushButton_final_base_price = self.widget.findChild(QPushButton, "pushButton_final_base_price")

#         self.label_final_correction_sum = self.widget.findChild(QLabel, "label_final_correction_sum")



#         self.groupBox_injener_correct = self.widget.findChild(QGroupBox, "groupBox_injener_correct")
#         self.groupBox_constructor_correct = self.widget.findChild(QGroupBox, "groupBox_constructor_correct")
#         self.groupBox_high_correct = self.widget.findChild(QGroupBox, "groupBox_high_correct")
#         self.table_structural_elements = self.widget.findChild(QTableWidget, "tableWidget_construction")
#         self.label_price_per_m2 = self.widget.findChild(QLabel, "label_price_per_m2")
#         self.pushButton_back_to_page_2 = self.widget.findChild(QPushButton, "pushButton_back_to_page_2")
#         self.pushButton_to_Page4 = self.widget.findChild(QPushButton, "pushButton_to_Page4")


#         # Сигналы
#         # self.table_structural_elements.keyPressEvent = self.handle_key_press
#         self.pushButton_to_Page4.clicked.connect(self.go_to_page4)
#         self.pushButton_back_to_page_2.clicked.connect(self.go_to_page2)
#         self.comboBox_facade.currentIndexChanged.connect(self.on_facade_selected)
#         self.setup_final_price_calculation()  # ✅ Привязываем кнопку к расчету итоговой стоимости

#         # Заполнение комбобокса
#         self.fill_facade_combobox()

    

#     def load_structural_elements(self, building_id):
#         """Загружает таблицу конструктивных элементов по ID здания."""
        
        
#         df = self.parent.data_service.structural_elements()
#         if df is None or df.empty:
#             QMessageBox.warning(self, "Ошибка", "Нет данных по конструктивным элементам.")
#             return
        
#         if building_id not in df.index:
#             QMessageBox.warning(self, "Ошибка", f"Нет данных для ID: {building_id}")
#             return
        
#         df_filtered = df.loc[[building_id], ["Конструкции", "Описание"]].copy()
        
#         # df_filtered["Поправка к удельным весам %"] = 0.0
#         # df_filtered["Физический износ %"] = 0.0
        
#         self.populate_table(df_filtered)


#     def populate_table(self, df):
#         """Отображает DataFrame в QTableWidget (только для чтения, без 'Доля %')."""
#         df = df.reset_index(drop=True)

#         # Убираем столбец "Доля %" из отображения
#         if "Доля %" in df.columns:
#             df = df.drop(columns=["Доля %"])

#         self.table_structural_elements.setRowCount(len(df))
#         self.table_structural_elements.setColumnCount(len(df.columns))
#         self.table_structural_elements.setHorizontalHeaderLabels(df.columns)

#         for row_idx, row in enumerate(df.itertuples(index=False)):
#             for col_idx, value in enumerate(row):
#                 item = QTableWidgetItem(str(value))
#                 item.setFlags(item.flags() & ~2)  # Все ячейки нередактируемые
#                 self.table_structural_elements.setItem(row_idx, col_idx, item)

#         # Растягиваем столбцы на всю ширину
#         self.table_structural_elements.resizeColumnsToContents()
#         header = self.table_structural_elements.horizontalHeader()
#         header.setStretchLastSection(True)
#         for i in range(df.shape[1]):
#             header.setSectionResizeMode(i, QHeaderView.Stretch)

  
        
    
    



#     def receive_building_data(self, building_id):
       
#         self.building_id = building_id
#         # Очищаем корректировки перед каждым пересчетом
#         self.improvement_correction = 0
#         self.deviation_correction = 0
#         self.facade_corrected_price = 0
#         self.high_corrected_price = 0

#         # Загружаем конструктивные элементы
#         self.load_structural_elements(building_id)

#         # Берём стоимость прямо из QLabel и извлекаем число
#         price_text = self.label_price_per_m2.text()
#         try:
#             # Пробуем извлечь число из метки
#             number_part = price_text.split(':')[-1].strip().replace(" ", "").replace(",", ".")
#             price_value = float(number_part)
            
#         except ValueError:
#             # Если не удалось, попробуем взять из данных литера
            
#             price_value = getattr(self, "final_cost", 0.0)
          


#         # Применяем улучшения и рассчитываем новую стоимость за м²
#         corrected_price_per_m2, applied_improvements = self.apply_improvements_logic(building_id, price_value)

        

#         # Обновляем groupBox с применёнными улучшениями
#         self.update_groupbox_improvements(applied_improvements, corrected_price_per_m2)
#         self.show_deviation_checkboxes(building_id)





#     def handle_key_press(self, event):
#         """Обрабатывает нажатие клавиши Enter и стрелок для перемещения по ячейкам."""
#         current_row = self.table_structural_elements.currentRow()
#         current_column = self.table_structural_elements.currentColumn()
        
#         if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
#             if current_column in [3, 4]:  # Разрешаем Enter только в редактируемых столбцах
#                 next_row = current_row + 1
#                 if next_row < self.table_structural_elements.rowCount():
#                     self.table_structural_elements.setCurrentCell(next_row, current_column)
#         elif event.key() == Qt.Key_Up:
#             self.table_structural_elements.setCurrentCell(max(0, current_row - 1), current_column)
#         elif event.key() == Qt.Key_Down:
#             self.table_structural_elements.setCurrentCell(min(self.table_structural_elements.rowCount() - 1, current_row + 1), current_column)
#         else:
#             QWidget.keyPressEvent(self.table_structural_elements, event)
   
   
   
#     def update_total_row(self):
#         """Обновляет строку 'Всего' при изменении значений."""
#         row_idx = self.table_structural_elements.rowCount() - 1
#         total_share = 0
#         total_adjustment = 0
#         avg_wear_sum = 0
#         count = 0

#         for row in range(row_idx):
#             try:
#                 share = self.table_structural_elements.item(row, 1)
#                 adjustment = self.table_structural_elements.item(row, 3)
#                 wear = self.table_structural_elements.item(row, 4)

#                 total_share += float(share.text()) if share and share.text() else 0
#                 total_adjustment += float(adjustment.text()) if adjustment and adjustment.text() else 0
#                 avg_wear_sum += float(wear.text()) if wear and wear.text() else 0
#                 count += 1
#             except (ValueError, AttributeError):
#                 continue

#         avg_wear = avg_wear_sum / count if count else 0

#         # Отключение сигнала для предотвращения рекурсии
#         self.table_structural_elements.blockSignals(True)

#         self.table_structural_elements.setItem(row_idx, 1, QTableWidgetItem(str(round(total_share, 2))))
#         self.table_structural_elements.setItem(row_idx, 3, QTableWidgetItem(str(round(total_adjustment, 2))))
#         self.table_structural_elements.setItem(row_idx, 4, QTableWidgetItem(str(round(avg_wear, 2))))

#         # Снова запрещаем редактировать строку "Всего"
#         for col in range(self.table_structural_elements.columnCount()):
#             item = self.table_structural_elements.item(row_idx, col)
#             if item:
#                 item.setFlags(item.flags() & ~Qt.ItemIsEditable)

#         self.table_structural_elements.blockSignals(False)


#     def go_to_page2(self):
#         """Переход на Page2"""
#         self.reset_deviations_ui()
#         self.parent.params_for_liter.setCurrentIndex(1)

#     def go_to_page4(self):
#         # Собираем данные перед переходом
#         page3_data = self.collect_page3_data()
#         self.parent.liter_data["page3"] = page3_data  # Сохраняем в общий словарь данных

#         collected_data = self.collect_page3_data()
        
#         """Переход на Page4"""
#         self.parent.page4.receive_building_data(self.building_id)  # Передаем building_id
#         self.parent.page4.populate_table()  # ← вызвать метод у Page4
#         self.parent.params_for_liter.setCurrentIndex(3)   

#     def apply_improvements_logic(self, building_id, price_per_m2):
#         """Применяет инженерные корректировки к цене и сохраняет сумму поправок"""
#         general_data = self.valuation_window.collect_general_data()

#         improvements_df = self.parent.data_service.Improvements()

#         if building_id not in improvements_df.index:
#             self.improvement_correction = 0
#             return price_per_m2, []

#         analog_improvements = improvements_df.loc[[building_id]]

#         improvements_mapping = {
#             'газификация': 'газификация',
#             'электроосвещение': 'электроосвещение',
#             'водоснабжение': 'водоснабжение',
#             'канализация': 'канализация',
#             'телефонная_линия': 'телефонная линия',
#             'электрический_водонагреватель': 'электрический водонагреватель',
#             'горячее_водоснабжение': 'горячее водоснабжение',
#             'отопление_печное': 'печное отопление',
#             'отопление_центральное': 'центральное отопление',
#             'отопление_АГВ': 'водяное отопление (АГВ, двухконтурный котёл)'
#         }

#         applied_improvements = []
#         total_percent = 0.0
#         heating_selected = general_data.get('отопление', '').lower()

#         central_correction_applied = False
#         central_heating_present = False
#         alternative_heating_selected = heating_selected in ['водяное отопление (агв, двухконтурный котёл)', 'печное отопление']

#         for _, row in analog_improvements.iterrows():
#             improvement_name = row['Улучшение']
#             has_improvement = row['Имеется']
#             correction_factor = row['Поправка']

#             # 📌 НЕ добавляем "Центральное отопление" сразу
#             if improvement_name.lower() == 'центральное отопление':
#                 central_heating_present = has_improvement == 1
#                 continue  # ⛔ НЕ добавляем эту корректировку в основном цикле!

#             elif improvement_name.lower() in ['печное отопление', 'водяное отопление (агв, двухконтурный котёл)']:
#                 if heating_selected == improvement_name.lower() and has_improvement == 0:
#                     applied_improvements.append((f'Наличие {improvement_name}', correction_factor))
#                     total_percent += correction_factor
#                 elif heating_selected != improvement_name.lower() and has_improvement == 1:
#                     applied_improvements.append((f'Отсутствие {improvement_name}', -correction_factor))
#                     total_percent -= correction_factor
#                 continue

#             for general_key, mapped_name in improvements_mapping.items():
#                 if mapped_name.lower() == improvement_name.lower():
#                     user_selected = general_data.get(general_key, False)

#                     if has_improvement == 0 and user_selected:
#                         applied_improvements.append((improvement_name, correction_factor))
#                         total_percent += correction_factor

#                     elif has_improvement == 1 and not user_selected:
#                         applied_improvements.append((improvement_name, -correction_factor))
#                         total_percent -= correction_factor
#                     break

#         # 📌 Теперь обрабатываем Центральное отопление отдельно, если нужно
#         if central_heating_present and alternative_heating_selected and not central_correction_applied:
#             correction_factor = analog_improvements[
#                 analog_improvements['Улучшение'].str.lower() == 'центральное отопление'
#             ]['Поправка'].values[0]

#             applied_improvements.append(('Отсутствие центрального отопления', -correction_factor))
#             total_percent -= correction_factor

#             # ✅ Проверяем, есть ли выбранное пользователем отопление в аналоге
#             selected_heating_row = analog_improvements[
#                 analog_improvements['Улучшение'].str.lower() == heating_selected
#             ]

#             if not selected_heating_row.empty:
#                 # Если отопление найдено в аналоге, берем его поправку
#                 selected_heating_correction = selected_heating_row['Поправка'].values[0]
#                 applied_improvements.append((f'Наличие {heating_selected}', selected_heating_correction))
#                 total_percent += selected_heating_correction
#             else:
#                 # Если отопления нет в аналоге, прибавляем стандартные 0.065
#                 applied_improvements.append(('Наличие альтернативного отопления ', 0.065))
#                 total_percent += 0.065

#             central_correction_applied = True  # ✅ Корректировка применена, больше не повторяется


#         # ✅ Рассчитываем итоговую сумму в деньгах
#         try:
#             price_str = self.label_price_per_m2.text().replace("Стоимость за м² по УКУП:", "").strip().split()[0]
#             base_price = float(price_str.replace(" ", "").replace(",", ""))
#             self.improvement_correction = base_price * total_percent
#         except Exception as e:
#             self.improvement_correction = 0
           

#         return price_per_m2, applied_improvements







#     # Чекбоксы для корректировок по абсолютным значениям
#     def show_deviation_checkboxes(self, building_id):
#         deviations_df = self.parent.data_service.Deviations()

#         if deviations_df is None or building_id not in deviations_df.index:
#             return

#         row = deviations_df.loc[building_id]

#         if self.groupBox_constructor_correct.layout() is None:
#             self.groupBox_constructor_correct.setLayout(QVBoxLayout())
#         layout = self.groupBox_constructor_correct.layout()

#         # Очистим старые чекбоксы
#         for i in reversed(range(layout.count())):
#             widget = layout.itemAt(i).widget()
#             layout.removeWidget(widget)
#             widget.setParent(None)

#         self.deviation_checkboxes = {}  # Храним ссылки на чекбоксы
#         self.deviation_correction = 0  # Начальная корректировка
#         self.label_deviation_result = QLabel("Коррекция: 0.00 сум")  # Метка для отображения корректировки
#         layout.addWidget(self.label_deviation_result)

#         for column, value in row.items():
#             if pd.notna(value) and str(value).strip() != '':
#                 checkbox = QCheckBox(f"{column}: {float(value):+.2f} сум")
#                 checkbox.stateChanged.connect(self.update_selected_deviations)
#                 layout.addWidget(checkbox)
#                 self.deviation_checkboxes[column] = (checkbox, float(value))


#     # это метод корректировки по абсолютным значениям
#     def update_selected_deviations(self):
#         if not hasattr(self, 'deviation_checkboxes'):
#             return
        
#         total_adjustment = 0.0
#         applied = []

#         for name, (checkbox, value) in self.deviation_checkboxes.items():
#             if checkbox.isChecked():
#                 total_adjustment += value
#                 applied.append((name, value))

#         self.deviation_correction = total_adjustment  # ✅ Обновляем сразу при выборе чекбоксов
#         self.label_deviation_result.setText(f"Коррекция: {total_adjustment:+.2f} сум")  # Обновляем отображение

        
        
       



    

#     def update_groupbox_improvements(self, applied_improvements, corrected_price_per_m2):
#         """Отображение примененных улучшений и итоговой цены в groupBox"""

#         # Проверяем, есть ли уже layout у groupBox, и если нет, создаём его.
#         if self.groupBox_injener_correct.layout() is None:
#             self.groupBox_injener_correct.setLayout(QVBoxLayout())

#         # Теперь, когда layout точно существует, можно очистить содержимое
#         layout = self.groupBox_injener_correct.layout()

#         for i in reversed(range(layout.count())):
#             widget_to_remove = layout.itemAt(i).widget()
#             layout.removeWidget(widget_to_remove)
#             widget_to_remove.setParent(None)
        
#         total_percent = 0.0

#         # Добавляем информацию по улучшениям
#         if applied_improvements:
#             for improvement, correction in applied_improvements:
#                 total_percent += correction
#                 correction_percent = correction * 100
#                 label = QLabel(f"{improvement}: {correction_percent:+.2f}%")
#                 layout.addWidget(label)
#         else:
#             label_no_improvements = QLabel("Корректировки не применялись")
#             layout.addWidget(label_no_improvements)

#         try:
#             price_str = self.label_price_per_m2.text().replace("Стоимость за м² по УКУП:", "").strip().split()[0]
#             base_price = float(price_str.replace(" ", "").replace(",", ""))
#             correction_amount = base_price * total_percent
#             label_total = QLabel(f"<b>Сумма всех инженерных корректировок: {correction_amount:,.2f} сум</b>")
#             layout.addWidget(label_total)
#         except Exception as e:
#             layout.addWidget(QLabel(f"Ошибка расчёта итоговой суммы: {e}"))
        



# #     
        


#     def fill_facade_combobox(self):
#         if self.facade_data is not None:
#             facade_types = self.facade_data['facade_type'].dropna().unique()
#             self.comboBox_facade.addItem("Выберите фасад")
#             self.comboBox_facade.addItems(facade_types)
#         else:
#             QMessageBox.warning(self, "Ошибка", "Таблица фасадов не загружена.")

#     def on_facade_selected(self, index):
#         if self.building_id is None:
#             return
#         if index == 0:
#             self.facade_corrected_price = 0  # ✅ Устанавливаем в 0, если фасад не выбран
#             self.label_facade_result.setText("Фасад не выбран")
#             return

#         # Применяется только к ID 1–136 и 140–155
#         if not (1 <= self.building_id <= 136 or 140 <= self.building_id <= 155):
#             self.facade_corrected_price = 0  # ✅ Обнуляем, если фасад не применяется
#             self.label_facade_result.setText("Поправка на фасад не применяется для данного типа здания")
#             return

#         selected_type = self.comboBox_facade.currentText()
#         row = self.facade_data[self.facade_data['facade_type'] == selected_type]

#         if row.empty:
#             QMessageBox.warning(self, "Ошибка", f"Не найдена запись для фасада: {selected_type}")
#             self.facade_corrected_price = 0  # ✅ Устанавливаем 0, если фасад не найден
#             return

#         try:
#             percent = row['%'].values[0]
#             price_str = self.label_price_per_m2.text().replace("Стоимость за м² по УКУП:", "").strip().split()[0]
#             price = float(price_str.replace(",", "").replace(" ", ""))
#             self.facade_corrected_price = price * percent  # ✅ Расчет корректировки

#             self.label_facade_result.setText(
#                 f"Стоимость корректировки на улучшение фасада: {self.facade_corrected_price:,.2f} сум"
#             )
#         except Exception as e:
#             QMessageBox.warning(self, "Ошибка", f"Не удалось применить корректировку: {e}")
#             self.facade_corrected_price = 0  # ✅ Устанавливаем 0 в случае ошибки



#     def high_correction(self, index=None):
#         try:
#             # Применяется только к ID от 1 до 108
#             if not (1 <= self.building_id <= 108):
#                 self.label_fact_high.clear()
#                 self.label_correction.clear()
#                 self.label_high_result.setText("Поправка на высоту не применяется для данного типа здания")
#                 self.high_corrected_price = 0  # ✅ Всегда сбрасываем
#                 return

#             fact_high_value = float(self.fact_high.replace(',', '.'))

#             if fact_high_value < 2.4:
#                 koeff = 1.06
#             elif fact_high_value > 4.0:
#                 koeff = 0.9
#             else:
#                 filter_high_df = self.altitude_data[
#                     self.altitude_data['Полезная высота, м'] == fact_high_value
#                 ]
#                 if filter_high_df.empty:
#                     self.label_fact_high.clear()
#                     self.label_correction.clear()
#                     self.label_high_result.setText("Коэффициент для высоты не найден")
#                     self.high_corrected_price = 0
#                     return

#                 koeff = filter_high_df['Поправочный коэффициент'].values[0]

#             high_percent = (koeff-1) * 100
#             high_correction = f"{high_percent:.2f} %"

#             price_str = self.label_price_per_m2.text().replace("Стоимость за м² по УКУП:", "").strip().split()[0]
#             price_per_m2 = float(price_str.replace(",", "").replace(" ", ""))
#             high_correction_result = price_per_m2 * (koeff-1)

#             self.label_fact_high.setText(f"{fact_high_value:.2f} м")
#             self.label_correction.setText(high_correction)
#             self.label_high_result.setText(f"Стоимость корректировки на высоту: {high_correction_result:,.2f} сум")

#             self.high_corrected_price = high_correction_result  # ✅ Сохраняем исправленный результат

#         except Exception as e:
#             QMessageBox.warning(self, "Ошибка", f"Ошибка при расчёте поправки на высоту: {e}")
#             self.high_corrected_price = 0  # ✅ В случае ошибки не ломаем расчёты

          



#     def set_fact_high(self, fact_high, building_id=None):
#         if building_id is not None:
#             self.building_id = int(building_id)
#         self.fact_high = fact_high
#         self.label_fact_high.setText(f"Высота здания: {self.fact_high}")
#         self.high_correction()
       


#     def reset_deviations_ui(self):
#         # Сброс комбобокса фасада
#         self.comboBox_facade.setCurrentIndex(0)
#         self.label_facade_result.clear()

#         # Сброс группы по высоте
#         self.label_fact_high.clear()
#         self.label_correction.clear()
#         self.label_high_result.clear()

#         # Сброс итогов
#         if self.groupBox_injener_correct.layout():
#             layout = self.groupBox_injener_correct.layout()
#             for i in reversed(range(layout.count())):
#                 widget = layout.itemAt(i).widget()
#                 layout.removeWidget(widget)
#                 widget.setParent(None)

#         if self.groupBox_constructor_correct.layout():
#             layout = self.groupBox_constructor_correct.layout()
#             for i in reversed(range(layout.count())):
#                 widget = layout.itemAt(i).widget()
#                 layout.removeWidget(widget)
#                 widget.setParent(None)

#         # Сброс внутренних переменных
#         self.facade_corrected_price = None
#         self.high_corrected_price = None
#         self.deviation_checkboxes = {}



    
#     def get_total_adjusted_price(self):
#         """Рассчитывает итоговую цену с учетом всех корректировок."""
#         try:
#             self.high_correction()  # ✅ Принудительно обновляем корректировку перед расчетом

#             price_str = self.label_price_per_m2.text().replace("Стоимость за м² по УКУП:", "").strip().split()[0]
#             base_price = float(price_str.replace(" ", "").replace(",", ""))
            
#             total_price = (
#                 base_price
#                 + self.facade_corrected_price
#                 + self.improvement_correction
#                 + self.deviation_correction
#                 + self.high_corrected_price
#             )
            
            
#             # Обновляем UI
#             self.groupBox__final_price.setTitle(f"Итоговая стоимость: {total_price:,.2f} сум")
        
#         except Exception as e:
#             QMessageBox.warning(self, "Ошибка", f"Ошибка при расчете итоговой стоимости: {e}")


#     def setup_final_price_calculation(self):
#         """Привязываем кнопку к расчёту итоговой стоимости."""
#         self.pushButton_final_base_price.clicked.connect(self.get_total_adjusted_price)



#     def collect_page3_data(self):
#         """Собирает данные с третьей страницы (Page3)"""

#         # Данные о фасаде
#         facade_data = {
#             "type": self.comboBox_facade.currentText(),
#             "corrected_price": self.facade_corrected_price
#         }

#         # Данные о высоте
#         high_data = {
#             "fact_high": self.label_fact_high.text(),
#             "correction": self.label_correction.text(),
#             "high_corrected_price": self.high_corrected_price
#         }

#         # Данные об инженерных корректировках
#         improvement_data = []
#         if self.groupBox_injener_correct.layout():
#             for i in range(self.groupBox_injener_correct.layout().count()):
#                 item = self.groupBox_injener_correct.layout().itemAt(i).widget()
#                 if isinstance(item, QLabel):
#                     improvement_data.append(item.text())

#         # Данные об абсолютных корректировках (дефекты)
#         deviation_data = []
#         if self.groupBox_constructor_correct.layout():
#             for i in range(self.groupBox_constructor_correct.layout().count()):
#                 item = self.groupBox_constructor_correct.layout().itemAt(i).widget()
#                 if isinstance(item, QCheckBox) and item.isChecked():
#                     deviation_data.append(item.text())

#         # Данные из таблицы конструктивных элементов
#         structural_data = []
#         for row in range(self.table_structural_elements.rowCount()):
#             row_data = {}
#             for col in range(self.table_structural_elements.columnCount()):
#                 item = self.table_structural_elements.item(row, col)
#                 if item:
#                     row_data[self.table_structural_elements.horizontalHeaderItem(col).text()] = item.text()
#             structural_data.append(row_data)

#         # Итоговая стоимость
#         total_price = self.groupBox__final_price.title().replace("Итоговая стоимость: ", "").strip()

#         collected_data = {
#             "facade_data": facade_data,
#             "high_data": high_data,
#             "improvement_data": improvement_data,
#             "deviation_data": deviation_data,
#             "structural_data": structural_data,
#             "total_price": total_price
#         }

        

#         return collected_data




    
#     def load_data(self, data):
#         """Загружает данные на третью страницу (Page3)"""
#         try:
#             # Загрузка данных о фасаде
#             facade_data = data.get("facade_data", {})
#             facade_type = facade_data.get("type", "Выберите фасад")
#             corrected_price = facade_data.get("corrected_price", 0)

#             index = self.comboBox_facade.findText(facade_type)
#             if index != -1:
#                 self.comboBox_facade.setCurrentIndex(index)
#             self.facade_corrected_price = corrected_price
#             self.label_facade_result.setText(
#                 f"Стоимость корректировки на улучшение фасада: {corrected_price:,.2f} сум"
#             )

#             # Загрузка данных о высоте
#             high_data = data.get("high_data", {})
#             self.label_fact_high.setText(high_data.get("fact_high", ""))
#             self.label_correction.setText(high_data.get("correction", ""))
#             self.high_corrected_price = high_data.get("high_corrected_price", 0)
#             self.label_high_result.setText(
#                 f"Стоимость корректировки на высоту: {self.high_corrected_price:,.2f} сум"
#             )

#             # Загрузка инженерных улучшений
#             improvement_data = data.get("improvement_data", [])
#             if self.groupBox_injener_correct.layout() is None:
#                 self.groupBox_injener_correct.setLayout(QVBoxLayout())
#             layout = self.groupBox_injener_correct.layout()
#             for improvement in improvement_data:
#                 label = QLabel(improvement)
#                 layout.addWidget(label)

#             # Загрузка абсолютных корректировок (дефектов)
#             deviation_data = data.get("deviation_data", [])
#             if self.groupBox_constructor_correct.layout() is None:
#                 self.groupBox_constructor_correct.setLayout(QVBoxLayout())
#             layout = self.groupBox_constructor_correct.layout()
#             for deviation in deviation_data:
#                 checkbox = QCheckBox(deviation)
#                 checkbox.setChecked(True)
#                 layout.addWidget(checkbox)

#             # Загрузка данных конструктивных элементов
#             structural_data = data.get("structural_data", [])
#             self.table_structural_elements.setRowCount(len(structural_data))
#             for row, row_data in enumerate(structural_data):
#                 for col, (header, value) in enumerate(row_data.items()):
#                     item = QTableWidgetItem(str(value))
#                     self.table_structural_elements.setItem(row, col, item)

#             # Загрузка итоговой стоимости
#             total_price = data.get("total_price", "0.00")
#             self.groupBox__final_price.setTitle(f"Итоговая стоимость: {total_price} сум")

            

#         except Exception as e:
#             QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные на третью страницу: {str(e)}")









        
        