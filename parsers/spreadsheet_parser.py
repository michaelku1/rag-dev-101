# parsers/spreadsheet_parser.py
import pandas as pd
from .base_parser import BaseParser

class SpreadsheetParser(BaseParser):
    def parse(self, file_path: str) -> str:
        df = pd.read_excel(file_path)
        return df.to_csv(index=False)  # simple example; can plug in more steps