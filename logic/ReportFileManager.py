import os
import json

class ReportFileManager:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.reports_dir = os.path.join(self.project_dir, "reports")

        # Создаём папку reports, если её нет
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)

    def get_report_path(self, report_number):
        """Возвращает путь к файлу отчёта"""
        return os.path.join(self.reports_dir, f"report_{report_number}.json")

    def create_report_file(self, report_number):
        """Создаёт новый пустой файл отчёта, если его нет"""
        report_path = self.get_report_path(report_number)
        if not os.path.exists(report_path):
            with open(report_path, "w", encoding="utf-8") as file:
                json.dump({}, file, ensure_ascii=False, indent=4)
        else:
            print("")

    def save_report_data(self, report_number, data):
        """Сохраняет данные отчёта в JSON-файл"""
        try:
            # Сохраняем отчет под новым номером
            report_path = self.get_report_path(report_number)
            with open(report_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print("")









    def load_report_data(self, report_number):
        """Загружает данные отчёта из JSON-файла"""
        try:
            report_path = self.get_report_path(report_number)
            if os.path.exists(report_path):
                with open(report_path, "r", encoding="utf-8") as file:
                    data = json.load(file)
                return data
            else:
                return {}
        except Exception as e:
            return {}
