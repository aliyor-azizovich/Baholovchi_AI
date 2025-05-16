import os
import json
from datetime import datetime

class ReportRegistry:
    def __init__(self, project_dir):
        self.project_dir = project_dir
        self.registry_path = os.path.join(self.project_dir, "data", "report_registry.json")

        # Если файла нет - создаём пустой реестр
        if not os.path.exists(self.registry_path):
            with open(self.registry_path, "w", encoding="utf-8") as file:
                json.dump({"reports": []}, file, ensure_ascii=False, indent=4)

    def load_registry(self):
        # Проверяем на пустоту и корректность данных
        try:
            with open(self.registry_path, "r", encoding="utf-8") as file:
                content = file.read().strip()
                if not content:
                    raise ValueError("Файл реестра пуст")
                return json.loads(content)
        except json.JSONDecodeError:
            return {"reports": []}
        except ValueError as e:
            return {"reports": []}
    
    def remove_report(self, report_number):
        """Удаляет отчет по номеру из реестра"""
        data = self.load_registry()
        reports = data.get("reports", [])

        # Фильтруем отчеты, исключая тот, который нужно удалить
        updated_reports = [report for report in reports if str(report.get("report_number")) != str(report_number)]

        # Проверяем, был ли отчет найден и удален
        if len(reports) == len(updated_reports):
            raise ValueError(f"Отчёт №{report_number} не найден в реестре.")

        # Обновляем данные и сохраняем в файл
        data["reports"] = updated_reports
        try:
            with open(self.registry_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            raise ValueError(f"Ошибка при сохранении реестра после удаления: {str(e)}")

        # Также удаляем сам файл отчета
        report_path = os.path.join("reports", f"report_{report_number}.json")
        if os.path.exists(report_path):
            try:
                os.remove(report_path)
            except Exception as e:
                print("")


    def add_report(self, report_number, reg_number, report_date, owner_name, buyer_name, adress, valuation_cost="Оценка не окончена"):
        # Загружаем текущие данные из реестра
        data = self.load_registry()

        # Создаём структуру нового отчёта
        new_report = {
            "report_number": report_number,
            "reg_number": reg_number,
            "report_date": report_date,
            "last_change_date": datetime.now().strftime("%Y-%m-%d"),
            "owner_name": owner_name,
            "buyer_name": buyer_name,
            "adress": adress,
            "valuation_cost": valuation_cost,  # Добавляем оценочную стоимость,
            "file_path": f"reports/report_{report_number}.json"
        }

        # Добавляем новый отчёт
        data["reports"].append(new_report)

        # Сохраняем обновлённые данные
        with open(self.registry_path, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)


    def update_report(self, report_number, reg_number, report_date, last_change_date, owner_name, buyer_name, adress, valuation_cost="Оценка не окончена"):
        try:
            # Загружаем существующие данные
            registry_path = os.path.join(self.project_dir, "data", "report_registry.json")
            with open(registry_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Ищем отчёт по номеру и обновляем данные
            updated = False
            for report in data.get("reports", []):
                if report.get("report_number") == report_number:
                    report['reg_number'] = reg_number
                    report["report_date"] = report_date
                    report["last_change_date"] = last_change_date
                    report["owner_name"] = owner_name
                    report["buyer_name"] = buyer_name
                    report["adress"] = adress
                    report["valuation_cost"] = valuation_cost
                    updated = True
                    break

            # Добавляем новый отчет, если не найден
            if not updated:
                new_report = {
                    "report_number": report_number,
                    'reg_number': reg_number,
                    "report_date": report_date,
                    "last_change_date": last_change_date,
                    "owner_name": owner_name,
                    "buyer_name": buyer_name,
                    "adress": adress,
                    "valuation_cost": valuation_cost
                }
                data["reports"].append(new_report)

            # Сохраняем обновлённые данные
            with open(registry_path, "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print("")


    def get_report_data(self, report_number):
        try:
            # Путь к файлу реестра
            registry_path = os.path.join(self.project_dir, "data", "report_registry.json")

            # Загружаем данные из реестра
            with open(registry_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Ищем отчёт по номеру
            for report in data.get("reports", []):
                if report["report_number"] == str(report_number):
                    return report

            return None
        except Exception as e:
            return None

    