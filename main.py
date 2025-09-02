from parsers.parser_factory import ParserFactory

def process_file(file_path: str, file_type: str):
    parser = ParserFactory.get_parser(file_type)
    text = parser.parse(file_path)
    # now you can pass `text` into embeddings / vector DB etc.
    return text

if __name__ == "__main__":
    txt1 = process_file("data/sample.xlsx", "spreadsheet")
    txt2 = process_file("data/report.pdf", "pdf")