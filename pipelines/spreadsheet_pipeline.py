from parsers.spreadsheet_parser import SpreadsheetParser
from .base_pipeline import BasePipeline

class SpreadsheetPipeline(BasePipeline):
    def __init__(self):
        self.parser = SpreadsheetParser()

    def run(self, file_path: str) -> str:
        text = self.parser.parse(file_path)
        # custom processing for spreadsheets (clean headers, merge scattered tables, etc.)
        return text