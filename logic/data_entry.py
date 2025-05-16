import os
import pandas as pd
from PyQt5.QtWidgets import QWidget

class DataEntryForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def load_stat_koeff(self):
        """Загружает данные коэффициентов из файла stat_koeff.xlsx"""
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, "../data/stat_koeff.xlsx")
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            return pd.DataFrame()

    
    def load_regional_coff(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, f"../data/regional_coff.xlsx")
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            return None
        
    def territorial_correction(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, f"../data/territorial correction.xlsx")
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            return None
        
    def province_choose(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, "../data/province_choose.xlsx")
            df = pd.read_excel(file_path, dtype={"kadastr": str})
            df["kadastr"] = df["kadastr"].str.strip().str.zfill(2)  # Удаляем пробелы и добавляем ведущие нули
            return df
        except Exception as e:
            print(f"[ERROR] Ошибка при загрузке province_choose: {e}")
            return None

        
    def ukup(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, f"../data/UKUP.parquet")
            df = pd.read_parquet(file_path)
            return df
        except Exception as e:
            return None
        
    def description(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, "../data/Description.parquet")
            df = pd.read_parquet(file_path)

            # Исправление: привести индекс к int
            df.index = df.index.astype(int)
            return df
        except Exception as e:
            return None

    def structural_elements(self):
            try:
                base_path = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_path, "../data/structural_elements.parquet")
                df = pd.read_parquet(file_path)

                # Исправление: привести индекс к int
                df.index = df.index.astype(int)
                return df
            except Exception as e:
                return None

    def Improvements(self):
            try:
                base_path = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_path, "../data/Improvements.parquet")
                df = pd.read_parquet(file_path)

                # Исправление: привести индекс к int
                df.index = df.index.astype(int)
                return df
            except Exception as e:
                return None
                
    def Deviations(self):
            try:
                base_path = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_path, "../data/Deviations.parquet")
                df = pd.read_parquet(file_path)

                # Исправление: привести индекс к int
                df.index = df.index.astype(int)
                return df
            except Exception as e:
                return None
    def facade(self):
            try:
                base_path = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_path, "../data/facade.parquet")
                df = pd.read_parquet(file_path)

                # Исправление: привести индекс к int
                df.index = df.index.astype(int)
                return df
            except Exception as e:
                return None        
    def altitude(self):
            try:
                base_path = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_path, "../data/altitude.parquet")
                df = pd.read_parquet(file_path)

                # Исправление: привести индекс к int
                df.index = df.index.astype(int)
                return df
            except Exception as e:
                return None                



    def rent_temp(self):
            try:
                base_path = os.path.dirname(os.path.abspath(__file__))
                file_path = os.path.join(base_path, "../data/rent_temp.csv")
                df = pd.read_csv(file_path)

                # Исправление: привести индекс к int
                # df.index = df.index.astype(int)
                return df
            except Exception as e:
                return None
            
    def load_rent_2025(self):
        """Загружает данные коэффициентов из файла stat_koeff.xlsx"""
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, "../data/rent_min_2025.xlsx")
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            return pd.DataFrame()
        



    def sesmos(self):
        try:
            base_path = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_path, f"../data/sesmos.xlsx")
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            return None