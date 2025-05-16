# from PyQt5.QtWidgets import QWidget, QMessageBox, QGridLayout, QCheckBox, QPushButton, QLabel, QGroupBox


# class Page1BuildingSelection(QWidget):
#     def __init__(self, widget, parent=None, service=None):
#         super().__init__(parent)
#         self.widget = widget
#         self.parent = parent  # Это LiterFilterDialog
#         self.service = service

#         # Сетка для чекбоксов
#         groupbox = self.widget.findChild(QGroupBox, "groupBox_buildings")
#         self.layout_checkboxes = groupbox.findChild(QGridLayout, "gridLayout_for_checkboxes")


#         self.checkboxes = []
#         self.load_building_types()

#         # Кнопка "ОК"
#         self.pushButton_ok = self.widget.findChild(QPushButton, "pushButton_ok")
#         self.pushButton_ok.clicked.connect(self.accept_data)
#         # Кнопка "Cancel"
        

#         # Лейблы
#         self.label_selected_building = self.findChild(QLabel, "label_selected_building")
        


#     def load_building_types(self):
#         """Заполняет чекбоксы уникальными типами зданий"""
#         buildings = self.service.get_unique_buildings()
#         row, col, max_rows = 0, 0, 7
#         for building in buildings:
#             cb = QCheckBox(building)
#             self.layout_checkboxes.addWidget(cb, row, col)
#             cb.clicked.connect(self.single_selection)  # Только один чекбокс
#             self.checkboxes.append(cb)
#             row += 1
#             if row >= max_rows:
#                 row, col = 0, col + 1

#     def single_selection(self):
#         """Выбор только одного чекбокса"""
#         sender = self.sender()
#         for cb in self.checkboxes:
#             if cb != sender:
#                 cb.setChecked(False)

#     def accept_data(self):
#         """Сохраняет выбранное здание и передает данные на вторую страницу"""
#         selected = [cb.text() for cb in self.checkboxes if cb.isChecked()]
#         if not selected:
#             QMessageBox.warning(self.widget, "Ошибка", "Выберите тип здания!")
#             return
#         building_type = selected[0]
      
#      # 🔥 Вызов метода collect_data для сбора актуальных данных
#         collected_data = self.collect_data()
       
    
#         # Сохраняем данные на первой странице в общий словарь liter_data
#         self.parent.liter_data["page1"] = collected_data

#         # Сохраняем в родительский диалог
#         self.parent.selected_building_type = building_type

#         # Переход на вторую страницу
#         self.parent.params_for_liter.setCurrentIndex(1)

#         # Передаем данные на вторую страницу (вызов метода родителя)
#         self.parent.load_page2_data(building_type)


        
#     def collect_data(self):
#         """Собирает данные с первой страницы (тип здания)"""
#         selected = [cb.text() for cb in self.checkboxes if cb.isChecked()]
#         if not selected:
#             QMessageBox.warning(self.widget, "Ошибка", "Выберите тип здания!")
#             return {}

#         building_type = selected[0]
#         # building_id = self.service.get_building_id(building_type)  # Если ID тоже нужен

#         data = {
#             "building_type": building_type,
#             # "building_id": building_id  # Если требуется
#         }

#         return data
    

    
#     def load_data(self, data):
#         """Загружает данные на первой странице (Page1)"""
#         try:
#             building_type = data.get("building_type", "")
#             found = False

#             # Ищем чекбокс с нужным текстом
#             for cb in self.checkboxes:
#                 if cb.text() == building_type:
#                     cb.setChecked(True)
#                     self.label_selected_building.setText(building_type)
#                     found = True
#                     break

#             if not found:
              
#                 return False

           
#             return True

#         except Exception as e:
          
#             return False


