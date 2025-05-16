# from PyQt5.QtWidgets import QDialog, QStackedWidget, QPushButton, QMessageBox
# from PyQt5 import uic
# import os
# import json
# # Импорт страниц
# from .pages.page1_building_selection import Page1BuildingSelection
# from .pages.Page2Filtering import Page2Filtering
# from .pages.page_3_deviations import page_3_deviations
# from .pages.page_4_final import Page4Final

# from logic.liter_logic import LiterFilterService


# class LiterFilterDialog(QDialog):
#     def __init__(self, parent=None, data_service=None, main_window=None, valuation_window=None, is_edit_mode=False):
#         super().__init__(parent)
#         uic.loadUi(os.path.join(os.path.dirname(__file__), "liter_choose_window.ui"), self)

#         self.data_service = data_service
#         self.service = LiterFilterService(self.data_service)
#         self.selected_building_type = None
#         self.main_window = main_window
#         self.valuation_window = valuation_window    # ValuationMainWindow (для comboBox, данных UI и т.п.)

#         self.project_dir = self.main_window.project_dir

#         self.is_edit_mode = is_edit_mode  # Задаем режим работы

#         # Находим stackedWidget
#         self.params_for_liter = self.findChild(QStackedWidget, "params_for_liter")

#         # Получаем доступ к страницам
#         self.page1_widget = self.params_for_liter.widget(0)
#         self.page1 = Page1BuildingSelection(self.page1_widget, self, self.service)
#         self.page3_widget = self.params_for_liter.widget(2)
#         self.page3 = page_3_deviations(
#             widget=self.page3_widget,
#             parent=self,
#             main_window=self.main_window,
#             valuation_window=self.valuation_window  # ← передаём сюда
#         )
#         self.page2_widget = self.params_for_liter.widget(1)
#         self.page2 = Page2Filtering(self.page2_widget, self, self.service)

        
#         self.page4_widget = self.params_for_liter.widget(3)
        
#         self.pushButton_cancel = self.findChild(QPushButton, "pushButton_cancel")
#         self.pushButton_cancel.clicked.connect(self.reject)
       
        
#         self.page4 = Page4Final(
#             self.page4_widget,
#             parent=self,
#             main_window=self.main_window,
#             valuation_window=self.valuation_window  # <-- передаём ссылку на ValuationMainWindow
#         )

#         self.liter_data = {}
            


#     def load_page2_data(self, building_type):
#         """Вызывается из первой страницы для передачи данных на вторую страницу"""
#         self.page2.load_filtered_data(building_type)
    
#     def collect_liter_data(self):
#         """Собирает данные из всех страниц в словарь"""
#         liter_data = {
#             "page1": self.page1.collect_data(),
#             "page2": self.page2.collect_data(),
#             "page3": self.page3.collect_page3_data(),
#             "page4": self.page4.collect_page4_data()
#         }
#         return liter_data


#     def load_liter_data(self, liter_data):
#         """Загружает данные выбранного литера в окно."""
#         try:
#             # Сохраняем данные литера в атрибут
#             self.liter_data = liter_data

#             # Попробуем загрузить данные на Page1
#             if not self.page1.load_data(liter_data.get("page1", {})):
#                 self.params_for_liter.setCurrentIndex(0)
#                 return
            

#             # Попробуем загрузить данные на Page2
#             if "page2" in liter_data:
#                 if not self.page2.load_data(liter_data.get("page2", {})):
#                     self.params_for_liter.setCurrentIndex(1)
#                     return
#             else:
#                 # Если данных нет, инициируем стандартную фильтрацию (как при новом литере)
#                 building_type = liter_data.get("page1", {}).get("building_type", "")
#                 self.parent.load_page2_data(building_type)

#             # Попробуем загрузить данные на Page3
#             if not self.page3.load_data(liter_data.get("page3", {})):
#                 self.params_for_liter.setCurrentIndex(2)
#                 return
            

#             # Попробуем загрузить данные на Page4
#             if not self.page4.load_data(liter_data.get("page4", {})):
#                 self.params_for_liter.setCurrentIndex(3)
#                 return
            

#         except Exception as e:
#             QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные литера: {str(e)}")


#     def save_liters_to_file(self):
#         """Сохраняет данные всех литеров в JSON-файл"""
        
#         try:
#             main_window = self.main_window

#             # Получаем номер отчета
#             report_number = self.valuation_window.report_number_input.text()
            
#             # Получаем путь к файлу отчета
#             file_path = os.path.join(self.project_dir, "reports", f"report_{report_number}.json")

#             # Структура данных для сохранения
#             data_to_save = {
#                 "report_number": report_number,
#                 "liters": main_window.saved_liters
#             }

#             # Если файл уже существует, обновляем его
#             if os.path.exists(file_path):
#                 with open(file_path, "r", encoding="utf-8") as file:
#                     existing_data = json.load(file)
#                 # Обновляем данные литеров
#                 existing_data["liters"] = main_window.saved_liters
#             else:
#                 existing_data = data_to_save

#             # Сохранение в файл
#             with open(file_path, "w", encoding="utf-8") as file:
#                 json.dump(existing_data, file, ensure_ascii=False, indent=4)

#             # print(f"✅ Данные литеров успешно сохранены в файл: {file_path}")
#         except Exception as e:
#             print(f"Ошибка при сохранении данных литеров: {str(e)}")


    