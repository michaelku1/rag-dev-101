from .spreadsheet_parser import SpreadsheetParser
from .pdf_parser import PDFParser

# similar to the adapter pattern
class ParserFactory:
    @staticmethod
    def get_parser(file_type: str):
        if file_type == "spreadsheet":
            return SpreadsheetParser()
        elif file_type == "pdf":
            return PDFParser()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")