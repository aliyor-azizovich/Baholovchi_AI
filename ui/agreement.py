from PyQt5.QtWidgets import (QWidget, QSpinBox, QCheckBox, QTableWidget, QPushButton, QLabel,
                            QDialog, QMessageBox, QTableWidgetItem, QLineEdit, QComboBox, QTextBrowser)
from PyQt5 import uic
import os

from PyQt5.QtGui import QFont
from ui.cost_method_dialogs.building_choose import BuildingChooseDialog
from ui.cost_method_dialogs.deviations_and_wear_dialog import DeviationsAndWearDialog

from logic.data_entry import DataEntryForm
from PyQt5.QtCore import QDate, Qt
import json
import pandas as pd
from functools import partial

import traceback

class AgreementWidget(QWidget):
    def __init__(self, parent=None, main_window=None, valuation_window=None):
        super().__init__(parent)
        self.main_window = main_window
        self.valuation_window = valuation_window

        uic.loadUi(os.path.join(os.path.dirname(__file__), "agreement_widget.ui"), self)
        self.data_service = DataEntryForm()

        self.comboBox_agreement_list = self.findChild(QComboBox, 'comboBox_agreement_list')
        self.checkBox_cost = self.findChild(QCheckBox, 'checkBox_cost')
        # self.checkBox_income = self.findChild(QCheckBox, 'checkBox_income')
        self.checkBox_comparative = self.findChild(QCheckBox, 'checkBox_comparative')
        self.spinBox_cost_percent = self.findChild(QSpinBox, 'spinBox_cost_percent')
        # self.spinBox_income_percent = self.findChild(QSpinBox, 'spinBox_income_percent')
        self.spinBox_comparative_percent = self.findChild(QSpinBox, 'spinBox_comparative_percent')
        self.label_cost_weighted_average = self.findChild(QLabel, 'label_cost_weighted_average')
        # self.label_income_weighted_average = self.findChild(QLabel, 'label_income_weighted_average')
        self.label_comparative_weighted_average = self.findChild(QLabel, 'label_comparative_weighted_average')
        self.label_final_cost = self.findChild(QLabel, 'label_final_cost')
        self.label_building_land = self.findChild(QLabel, 'label_building_land')
        self.pushButton_final_save = self.findChild(QPushButton, 'pushButton_final_save')
        self.pushButton_final_save.clicked.connect(self.final_save)
        self.pushButton_upload_report = self.findChild(QPushButton, 'pushButton_upload_report')

        self.comboBox_agreement_list.addItems(['Взвешенное среднее', 'Среднее арифметическое'])
        self.comboBox_agreement_list.setCurrentText('Взвешенное среднее')

        self.checkBox_cost.setChecked(True)
        # self.checkBox_income.setChecked(True)
        self.checkBox_comparative.setChecked(True)
        self.checkBox_cost.stateChanged.connect(self.on_checkbox_state_changed)
        #self.checkBox_income.stateChanged.connect(self.on_checkbox_state_changed)
        self.checkBox_comparative.stateChanged.connect(self.on_checkbox_state_changed)

        # Установим начальные значения процентов
        self.spinBox_cost_percent.setValue(33)
        #self.spinBox_income_percent.setValue(33)
        self.spinBox_comparative_percent.setValue(34)

        self.checkBox_cost.stateChanged.connect(self.update_agreement_ui)
        #self.checkBox_income.stateChanged.connect(self.update_agreement_ui)
        self.checkBox_comparative.stateChanged.connect(self.update_agreement_ui)
        self.comboBox_agreement_list.currentTextChanged.connect(self.update_agreement_ui)

        self.spinBox_cost_percent.valueChanged.connect(lambda: self.redistribute_percent("cost"))
        # self.spinBox_income_percent.valueChanged.connect(lambda: self.redistribute_percent("income"))
        self.spinBox_comparative_percent.valueChanged.connect(lambda: self.redistribute_percent("comparative"))
        self.cost_value = 0
        #self.income_value = 0
        self.comparative_value = 0

       
        self.update_agreement_ui()

    def format_sum(self, value):
        return f"{round(value):,}".replace(",", " ")

   


    def load_costs_from_json(self, full_data):
        try:
            # Затратный подход
            liters = full_data.get("liters", [])
            building_cost = sum(liter.get("final_cost", 0) for liter in liters)

            land_text = full_data.get("land_valuation", {}).get("land_total_cost", "")
            land_cost = 0
            if land_text:
                land_cost = float(land_text.split(":")[-1].replace("сум", "").replace(" ", "").replace(",", ""))

            self.cost_value = building_cost + land_cost
            self.checkBox_cost.setText(
                f"Затратный подход: {self.format_sum(self.cost_value)} сум\n")
            self.label_building_land.setText(
                f"Стоимость улучшений: {self.format_sum(building_cost)} сум\n"
                f"Права на землю: {self.format_sum(land_cost)} сум"
            )



            # Доходный подход
            #income_text = full_data.get("income_valuation", {}).get("income_cost", "0")
            #self.income_value = float(income_text.replace(" ", "").replace(",", ""))
            #self.checkBox_income.setText(f"Доходный подход:\n{self.format_sum(self.income_value)} сум")

            # Сравнительный подход
            comp_text = full_data.get("comparative", {}).get("label_comparative_final_cost", "")
            comp_number = "".join(c for c in comp_text if c.isdigit() or c in ",.")
            self.comparative_value = float(comp_number.replace(" ", "").replace(",", "")) if comp_number else 0
            self.checkBox_comparative.setText(f"Сравнительный подход\n{self.format_sum(self.comparative_value)} сум")

            self.update_agreement_ui()

        except Exception as e:
            print("[ERROR] Ошибка загрузки стоимостей из JSON:", e)



    def update_agreement_ui(self):
        method = self.comboBox_agreement_list.currentText()
        use_cost = self.checkBox_cost.isChecked()
        #use_income = self.checkBox_income.isChecked()
        use_comparative = self.checkBox_comparative.isChecked()

        widgets = [
            (self.spinBox_cost_percent, self.label_cost_weighted_average, use_cost),
            # (self.spinBox_income_percent, self.label_income_weighted_average, use_income),
            (self.spinBox_comparative_percent, self.label_comparative_weighted_average, use_comparative),
        ]

        if sum([use_cost, use_comparative]) <= 1:
            for spin, label, _ in widgets:
                spin.setVisible(False)
                label.setVisible(False)
            self.label_final_cost.setText(self.get_single_cost(use_cost, use_comparative))
            return

        if method == 'Среднее арифметическое':
            for spin, label, active in widgets:
                spin.setVisible(False)
                label.setVisible(False)
            self.recalculate_average()
        else:
            for spin, label, active in widgets:
                spin.setVisible(active)
                label.setVisible(active)
            self.recalculate_weighted_average()

    def get_single_cost(self, use_cost, use_comparative):
        if use_cost and self.cost_value:
            return f"Итоговая стоимость: {self.format_sum(self.cost_value)} сум"
        # if use_income and self.income_value:
        #     return f"Итоговая стоимость: {self.format_sum(self.income_value)} сум"
        if use_comparative and self.comparative_value:
            return f"Итоговая стоимость: {self.format_sum(self.comparative_value)} сум"
        return "Итоговая стоимость: н/д"

    def recalculate_average(self):
        total = 0
        count = 0
        if self.checkBox_cost.isChecked() and self.cost_value:
            total += self.cost_value
            count += 1
        # if self.checkBox_income.isChecked() and self.income_value:
        #     total += self.income_value
        #     count += 1
        if self.checkBox_comparative.isChecked() and self.comparative_value:
            total += self.comparative_value
            count += 1
        if count:
            avg = total / count
            self.label_final_cost.setText(f"Итоговая стоимость: {self.format_sum(avg)} сум")
        else:
            self.label_final_cost.setText("Итоговая стоимость: н/д")

    def recalculate_weighted_average(self):
        parts = []
        total_percent = 0

        if self.checkBox_cost.isChecked() and self.cost_value is not None:
            p = self.spinBox_cost_percent.value()
            parts.append((self.cost_value, p, 'cost'))
            total_percent += p
        # if self.checkBox_income.isChecked() and self.income_value is not None:
        #     p = self.spinBox_income_percent.value()
        #     parts.append((self.income_value, p, 'income'))
        #     total_percent += p
        if self.checkBox_comparative.isChecked() and self.comparative_value is not None:
            p = self.spinBox_comparative_percent.value()
            parts.append((self.comparative_value, p, 'comparative'))
            total_percent += p

        if total_percent != 100:
            self.label_final_cost.setText("Ошибка: сумма процентов ≠ 100%")
            return

        weighted_total = sum(value * percent / 100 for value, percent, _ in parts)
        self.label_final_cost.setText(f"Итоговая стоимость: {self.format_sum(weighted_total)} сум")

        # Обновляем подписи с весовой стоимостью
        for value, percent, key in parts:
            portion = value * percent / 100
            text = f"{self.format_sum(portion)} сум"
            if key == 'cost':
                self.label_cost_weighted_average.setText(text)
            # elif key == 'income':
            #     self.label_income_weighted_average.setText(text)
            elif key == 'comparative':
                self.label_comparative_weighted_average.setText(text)


    def redistribute_percent(self, changed):
        if self.comboBox_agreement_list.currentText() != 'Взвешенное среднее':
            return

        all_boxes = {
            "cost": (self.checkBox_cost.isChecked(), self.spinBox_cost_percent),
            # "income": (self.checkBox_income.isChecked(), self.spinBox_income_percent),
            "comparative": (self.checkBox_comparative.isChecked(), self.spinBox_comparative_percent)
        }

        # Оставляем только активные подходы
        active = {k: box for k, (checked, box) in all_boxes.items() if checked}
        if len(active) <= 1:
            return  # Только один подход — не перераспределяем

        changed_box = active.get(changed)
        if changed_box is None:
            return

        changed_value = changed_box.value()
        others = {k: b for k, b in active.items() if k != changed}

        # === Два подхода — делим 100% между ними ===
        if len(active) == 2:
            for k, box in others.items():
                other_value = 100 - changed_value
                box.blockSignals(True)
                box.setValue(other_value)
                box.blockSignals(False)
            self.recalculate_weighted_average()
            return

        # === Три подхода — делим оставшееся между двух ===
        remaining = 100 - changed_value
        share = remaining // len(others)
        leftover = remaining % len(others)

        for i, (k, box) in enumerate(others.items()):
            val = share + (1 if i == 0 and leftover > 0 else 0)
            box.blockSignals(True)
            box.setValue(val)
            box.blockSignals(False)

        self.recalculate_weighted_average()





    def on_checkbox_state_changed(self):
        if self.comboBox_agreement_list.currentText() != 'Взвешенное среднее':
            return

        active_boxes = {
            "cost": self.spinBox_cost_percent if self.checkBox_cost.isChecked() else None,
            # "income": self.spinBox_income_percent if self.checkBox_income.isChecked() else None,
            "comparative": self.spinBox_comparative_percent if self.checkBox_comparative.isChecked() else None
        }

        active_boxes = {k: box for k, box in active_boxes.items() if box is not None}
        count = len(active_boxes)

        if count == 3:
            # Устанавливаем строго базовое распределение
            default_distribution = {
                "cost": 50,
                # "income": 33,
                "comparative": 50
            }
            for k, box in active_boxes.items():
                box.blockSignals(True)
                box.setValue(default_distribution[k])
                box.blockSignals(False)
            self.recalculate_weighted_average()
            return

        elif count == 2:
            for box in active_boxes.values():
                box.blockSignals(True)
                box.setValue(50)
                box.blockSignals(False)
            self.recalculate_weighted_average()
            return

        elif count == 1:
            only_box = list(active_boxes.values())[0]
            only_box.blockSignals(True)
            only_box.setValue(100)
            only_box.blockSignals(False)
            self.recalculate_weighted_average()
            return


    def collect_agreement_data(self):
        return {
            "method": self.comboBox_agreement_list.currentText(),
            "use_cost": self.checkBox_cost.isChecked(),
            # "use_income": self.checkBox_income.isChecked(),
            "use_comparative": self.checkBox_comparative.isChecked(),
            "cost_percent": self.spinBox_cost_percent.value(),
            # "income_percent": self.spinBox_income_percent.value(),
            "comparative_percent": self.spinBox_comparative_percent.value(),
            'final_cost': self.label_final_cost.text()
           }


    def load_agreement_data(self, data):
        try:
            self.comboBox_agreement_list.setCurrentText(data.get("method", "Взвешенное среднее"))
            self.checkBox_cost.setChecked(data.get("use_cost", True))
            # self.checkBox_income.setChecked(data.get("use_income", True))
            self.checkBox_comparative.setChecked(data.get("use_comparative", True))
            self.spinBox_cost_percent.setValue(data.get("cost_percent", 33))
            # self.spinBox_income_percent.setValue(data.get("income_percent", 33))
            self.spinBox_comparative_percent.setValue(data.get("comparative_percent", 34))

            self.cost_value = float(data.get("cost_value", 0))
            # self.income_value = float(data.get("income_value", 0))
            self.comparative_value = float(data.get("comparative_value", 0))

            self.checkBox_cost.setText(
                f"({self.format_sum(self.cost_value)} сум)\n\n")
            self.label_building_land.setText(
                f"Стоимость улучшений: ...\n\nПрава на землю: ..."
            )
            # self.checkBox_income.setText(f"{self.format_sum(self.income_value)} сум")
            self.checkBox_comparative.setText(f"{self.format_sum(self.comparative_value)} сум")
            self.update_agreement_ui()
        except Exception as e:
            print(f"[ERROR] Не удалось загрузить данные вкладки Согласование: {e}")



    def final_save(self):
        self.valuation_window.save_report()