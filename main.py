from parsers.parser_factory import ParserFactory

def process_file(file_path: str, file_type: str):
    pipeline = ParserFactory.get_pipeline(file_type)
    text = pipeline.run(file_path)
    # send text into embeddings/vector DB
    return text

if __name__ == "__main__":
    PATH = "/Users/michael/Desktop/eparse/simple-rag/sample_data/messy_crm_sales_one_sheet.xlsx"
    txt1 = process_file(PATH, "spreadsheet")
    # txt2 = process_file("data/report.pdf", "pdf")