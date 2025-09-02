# parsers/pdf_parser.py
import fitz  # PyMuPDF
from .base_parser import BaseParser

class PDFParser(BaseParser):
    def parse(self, file_path: str) -> str:
        doc = fitz.open(file_path)
        text = "\n".join(page.get_text() for page in doc)
        return text


