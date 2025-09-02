from parsers.pdf_parser import PDFParser
from .base_pipeline import BasePipeline

class PDFPipeline(BasePipeline):
    def __init__(self):
        self.parser = PDFParser()

    def run(self, file_path: str) -> str:
        text = self.parser.parse(file_path)
        # custom processing for PDFs (OCR, remove headers/footers, chunking, etc.)
        return text