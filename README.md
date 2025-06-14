# 🏠 ValuateApp – Приложение для оценки жилых домов

**ValuateApp** — это десктопное приложение, разработанное на Python (PyQt5), для автоматизации профессиональной оценки недвижимости. Поддерживает затратный, доходный и сравнительный подходы с возможностью генерации отчёта в формате Word.

---

## 🚀 Основные возможности

- ✅ Ввод характеристик объекта оценки
- 🏗️ Расчёт восстановительной стоимости (затратный подход)
- 💰 Доходный подход: аренда, убытки, дисконтирование
- 📊 Сравнительный анализ на основе аналогов с OLX.uz
- 🧮 Корректировки, физический и функциональный износ
- 📄 Генерация отчёта в формате DOCX
- 📂 Сохранение и восстановление отчётов (JSON)

---



## 🛠 Установка и запуск

> Требуется Python 3.9+  
> Убедитесь, что установлены все зависимости:

# В целях сохранения конфедициональности вся использованная база данных не включена в данный репозиторий. По всем вопросам обращаться по указанным контактам
  valuateapp/
  ├── main.py
  ├── ui/
  │   ├── main_window.py
  │   ├── data_entry.py
  │   ├── region_selection.py
  │   ├── liter_selection.py
  │   └── ...
  ├── logic/
  │   ├── database.py
  │   ├── calculations.py
  │   └── filters.py
  ├── data/
  │   ├── regions.xlsx
  │   ├── stat_koeff.xlsx
  │   └── УКУП.xlsx
  ├── README.md
  ├── requirements.txt


📦 Основные зависимости
PyQt5

pandas

openpyxl

python-docx

BeautifulSoup4

requests


📚 Законодательная основа
Программа соответствует требованиям:

📘 Единого Национального Стандарта Оценки (ЕНСО), 2023

📊 Методических рекомендаций Госкомстата Республики Узбекистан

🧑‍💻 Контакты
powered by: aliyor_azizovich

📧 aliyor.0276@gmail.com
📞 +998 99 990 02 76
📞 +998 91 206 02 76
