# from .spreadsheet_parser import SpreadsheetParser
# from .pdf_parser import PDFParser

from pipelines.spreadsheet_pipeline import SpreadsheetPipeline
from pipelines.pdf_pipeline import PDFPipeline

# similar to the adapter pattern
# class ParserFactory:
#     @staticmethod
#     def get_parser(file_type: str):
#         if file_type == "spreadsheet":
#             return SpreadsheetParser()
#         elif file_type == "pdf":
#             return PDFParser()
#         else:
#             raise ValueError(f"Unsupported file type: {file_type}")
        
class ParserFactory:
    @staticmethod
    def get_pipeline(file_type: str):
        if file_type == "spreadsheet":
            return SpreadsheetPipeline()
        elif file_type == "pdf":
            return PDFPipeline()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
        
