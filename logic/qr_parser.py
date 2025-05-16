import fitz  # PyMuPDF для работы с PDF
from pyzbar.pyzbar import decode
from PIL import Image
import io
import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from io import StringIO
from io import BytesIO
from logic.cadastral_number import EnterCaptchaDialog
from PyQt5.QtWidgets import QDialog

class QRParser:
    

    def extract_qr_from_report(self, report_folder, report_number):
        """Ищет файл кадастра и извлекает QR-код независимо от формата."""
        filename_base = f"Kadastr - Отчёт №{report_number}"
        for ext in ['.pdf', '.jpg', '.jpeg', '.png']:
            full_path = os.path.join(report_folder, filename_base + ext)
            if os.path.exists(full_path):
                if ext == '.pdf':
                    return self.extract_qr_from_pdf(full_path)
                else:
                    return self.extract_qr_from_image(full_path)
        print(f"⚠️ Файл кадастра для отчёта №{report_number} не найден в папке {report_folder}.")
        return None


    def fetch_data_from_link(self, url):
        """Переходит по ссылке и возвращает HTML текст."""
        try:
            response = requests.get(url, timeout=10)
            if response.ok:
                return response.text
            else:
                return None
        except Exception as e:
            print(f"Ошибка запроса: {str(e)}")
            return None

    
    def parse_data(self, html_text):
        """Парсит таблицу по фиксированным позициям строк."""

        if not html_text:
            return {}

        result = {}

        try:
            soup = BeautifulSoup(html_text, 'html.parser')

            # Ищем блок содержимого
            content_div = soup.find('div', class_="proerty_content")
            if not content_div:
                print("⚠️ Блок proerty_content не найден.")
                return {}

            # 1. Извлекаем кадастровый номер
            cadastral_number_tag = content_div.find(['h1', 'h3'], class_="captlize")
            if cadastral_number_tag:
                result["cadastral_number"] = cadastral_number_tag.get_text(strip=True)
                # print(f"✅ Извлечено: cadastral_number -> {result['cadastral_number']}")
            else:
                result["cadastral_number"] = "Не указан"

            # 2. Извлекаем адрес
            address_tag = content_div.find('p', class_="location-color")
            if address_tag:
                result["address"] = address_tag.get_text(strip=True)
                # print(f"✅ Извлечено: address -> {result['address']}")
            else:
                result["address"] = "Не указан"

            # 3. Ищем таблицу
            table = content_div.find('table')
            if not table:
                # print("⚠️ Таблица внутри блока не найдена.")
                return result

            rows = table.find_all('tr')

            for idx, row in enumerate(rows, start=1):
                cols = row.find_all('td')
                if len(cols) >= 2:
                    value_html = cols[1]
                    value_text = value_html.get_text(separator=" ", strip=True)

                    if idx == 1:
                        result["owner_name"] = value_text
                        # print(f"✅ Извлечено: owner_name (строка {idx}) -> {value_text}")

                    elif idx == 3:
                        result["land_area"] = self.clean_value("land_area", value_text)
                        # print(f"✅ Извлечено: land_area (строка {idx}) -> {result['land_area']}")

                    elif idx == 4:
                        result["usefull_area"] = self.clean_value("usefull_area", value_text)
                        # print(f"✅ Извлечено: usefull_area (строка {idx}) -> {result['usefull_area']}")

                    elif idx == 5:
                        result["living_area"] = self.clean_value("living_area", value_text)
                        # print(f"✅ Извлечено: living_area (строка {idx}) -> {result['living_area']}")

                    elif idx == 6:
                        result["total_area"] = self.clean_value("total_area", value_text)
                        # print(f"✅ Извлечено: total_area (строка {idx}) -> {result['total_area']}")

                    # Остальные строки можешь дополнительно обрабатывать при необходимости
                    # Например, кадастровую стоимость, номер выписки и т.д.

        except Exception as e:
            print(f"❌ Ошибка парсинга: {str(e)}")

        # 4. Заполняем пустые поля
        all_fields = ["cadastral_number", "address", "owner_name",
                    "land_area", "total_area", "usefull_area", "living_area"]

        for field in all_fields:
            if field not in result:
                result[field] = "Не указано"

        return result

    def parse_kochirma_data(self, html_text):
        """Парсит страницу 'Кўчирма', правильная финальная версия."""

        if not html_text:
            return {}

        result = {}

        try:
            soup = BeautifulSoup(html_text, 'html.parser')

            content_div = soup.find('div', class_="proerty_content")
            if not content_div:
                # print("⚠️ Блок proerty_content не найден.")
                return {}

            table = content_div.find('table')
            if not table:
                # print("⚠️ Таблица внутри блока не найдена.")
                return {}

            rows = table.find_all('tr')

            for idx, row in enumerate(rows, start=1):
                cols = row.find_all('td')
                if len(cols) < 2:
                    # print(f"⚠️ Строка {idx} пропущена: нет двух колонок")
                    continue

                key_html = cols[0]
                value_html = cols[1]
                key_text = key_html.get_text(separator=" ", strip=True).lower()
                value_text = value_html.get_text(separator=" ", strip=True)

                # 1. Извлекаем адрес
                if idx == 5:
                    result["address"] = value_text
                    # print(f"✅ Извлечено address (строка {idx}) -> {value_text}")

                # 2. Извлекаем владельца
                elif idx == 8:
                    owner_raw = value_text.split(',')[0].strip()
                    result["owner_name"] = owner_raw
                    # print(f"✅ Извлечено owner_name (строка {idx}) -> {owner_raw}")

                # 3. Извлекаем площадь земли
                elif "давлат рўйхатидан ўтказилган ер майдони" in key_text:
                    result["land_area"] = self.clean_value("land_area", value_text)
                    # print(f"✅ Извлечено land_area (строка {idx}) -> {result['land_area']}")

                # 4. Обрабатываем кадастр и площади (строения)
                elif "давлат рўйхатидан ўтказилган бино ва иншоотлар майдони" in key_text:
                    paragraphs = value_html.find_all('p')
                    for p in paragraphs:
                        p_text = p.get_text(separator=" ", strip=True)

                        # Кадастровый номер (без пробелов, много ':')
                        if ":" in p_text and p_text.count(":") >= 2 and " " not in p_text:
                            result["cadastral_number"] = p_text
                            # print(f"✅ Извлечено cadastral_number -> {p_text}")

                        # Полезная площадь
                        elif "умумий фойдаланиш майдони" in p_text.lower():
                            result["usefull_area"] = self.extract_number(p_text)
                            # print(f"✅ Извлечено usefull_area -> {result['usefull_area']}")

                        # Площадь застройки
                        elif "қурилиш ости майдони" in p_text.lower():
                            result["total_area"] = self.extract_number(p_text)
                            # print(f"✅ Извлечено total_area -> {result['total_area']}")

                        # Жилая площадь
                        elif "яшаш майдони" in p_text.lower():
                            result["living_area"] = self.extract_number(p_text)
                            # print(f"✅ Извлечено living_area -> {result['living_area']}")

        except Exception as e:
            print(f"❌ Ошибка парсинга кучирма: {str(e)}")

        # Заполняем пустые поля для стабильности
        all_fields = ["cadastral_number", "address", "owner_name",
                    "land_area", "total_area", "usefull_area", "living_area"]

        for field in all_fields:
            if field not in result:
                result[field] = "Не указано"

        return result





    def extract_number(self, text):
        """Извлекает первое число из текста."""
        import re
        match = re.search(r"(\d+[\.,]?\d*)", text)
        if match:
            num = match.group(1).replace(",", ".")
            try:
                return float(num)
            except:
                return None
        return None





    def clean_value(self, mapped_key, value):
        if mapped_key in ["land_area", "total_area", "living_area", "build_area", "occupied_land", "usefull_area"]:
            cleaned = value.replace("м2", "").replace("м 2", "").replace("м²", "").replace(" ", "").replace(",", ".")
            try:
                return float(cleaned)
            except:
                return "Не указано"

        if mapped_key == "cadastral_value":
            cleaned = value.replace("so'm", "").replace("сўм", "").replace("*", "").replace(" ", "").replace(",", ".")
            try:
                return int(float(cleaned))
            except:
                return "Не указано"

        return value




        return result
    def extract_qr_from_pdf(self, pdf_path):
        """Извлекает ссылку из QR-кода в PDF."""
        try:
            doc = fitz.open(pdf_path)
            for page in doc:
                pix = page.get_pixmap()
                img = Image.open(io.BytesIO(pix.tobytes("png")))
                decoded_objects = decode(img)
                for obj in decoded_objects:
                    if obj.type == 'QRCODE':
                        return obj.data.decode('utf-8')
        except Exception as e:
            print(f"Ошибка при считывании QR из PDF: {str(e)}")
        return None


    def extract_qr_from_image(self, image_path):
        """Извлекает ссылку из QR-кода в JPG/PNG."""
        try:
            img = Image.open(image_path)
            decoded_objects = decode(img)
            for obj in decoded_objects:
                if obj.type == 'QRCODE':
                    return obj.data.decode('utf-8')
        except Exception as e:
            print(f"Ошибка при считывании QR из изображения: {str(e)}")
        return None


    
    def search_by_cadastral_number(self, cadastral_number):
        """Ищет кадастр на сайте через заполнение формы с капчей."""
        try:
            session = requests.Session()

            # 1. Получаем главную страницу, чтобы достать токен и капчу
            home_page = session.get("https://davreestr.uz/uz", timeout=10)
            if not home_page.ok:
                print("Ошибка загрузки главной страницы")
                return None

            soup = BeautifulSoup(home_page.text, 'html.parser')

            # Ищем токен
            token_input = soup.find("input", {"name": "_token"})
            if not token_input:
                print("Токен не найден на странице")
                return None
            token = token_input.get("value")

            # Ищем капчу
            captcha_img = soup.find("div", {"class": "captcha"}).find("img")
            if not captcha_img:
                print("Картинка капчи не найдена")
                return None
            captcha_url = captcha_img.get("src")

            # Загружаем капчу
            captcha_response = session.get(captcha_url, timeout=10)
            if not captcha_response.ok:
                print("Ошибка загрузки капчи")
                return None

            # Показываем капчу пользователю через окно
            dialog = EnterCaptchaDialog(captcha_response.content)
            if dialog.exec_() == QDialog.Accepted:
                captcha_text = dialog.get_captcha_text()
                if not captcha_text:
                    print("Капча не введена пользователем")
                    return None
            else:
                print("Ввод капчи отменён пользователем")
                return None

            # 2. Теперь отправляем форму поиска
            payload = {
                "_token": token,
                "type": "cad_num",
                "cad_number": cadastral_number,
                "captcha": captcha_text
            }

            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Referer": "https://davreestr.uz/uz",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            }

            search_response = session.post("https://davreestr.uz/data/get-info/search", data=payload, headers=headers, timeout=10)

            if search_response.ok:
                return search_response.text
            else:
                print(f"Ошибка поиска кадастра: код ответа {search_response.status_code}")
                return None

        except Exception as e:
            print(f"Ошибка поиска кадастра: {str(e)}")
            return None