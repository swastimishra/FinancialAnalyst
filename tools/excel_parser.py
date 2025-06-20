import pandas as pd

class ExcelParserTool:
    @staticmethod
    def read(file_path):
        """Read an Excel file and return a pandas DataFrame."""
        return pd.read_excel(file_path, engine='openpyxl') 