import pandas as pd

def get_contiguous_blocks(df):
    """
    Given a DataFrame, returns a list of smaller DataFrames.
    Each block corresponds to a region of consecutive
    non-null values (row- and column-wise).
    """
    blocks = []
    current_block_rows = [] # keep track of block
    
    # NOTE 找non empty row index然後把它存下來
    for row_idx in range(len(df)):
        # check if the row has at least one non-null cell
        if df.iloc[row_idx].notnull().any():
            current_block_rows.append(row_idx)
        else:
            # NOTE 找blocks
            # if this is an empty row and we have collected rows for a block,
            # we finalize the current block
            if current_block_rows:
                # NOTE 用 index 來切block
                block = df.iloc[current_block_rows].dropna(axis=1, how='all')
                blocks.append(block)
                current_block_rows = []
    
    # In case the last rows were non-empty → produce a block
    if current_block_rows:
        block = df.iloc[current_block_rows].dropna(axis=1, how='all')
        blocks.append(block)
    
    return blocks

def chunk_excel_by_scattered_sections(path):
    xls = pd.ExcelFile(path)
    chunks = []
    
    for sheet_name in xls.sheet_names:
        # NOTE 這個方法專注在轉df
        df = xls.parse(sheet_name, header=None)

        # Get individual contiguous blocks within that sheet
        blocks = get_contiguous_blocks(df)

        for block in blocks:
            # Create a chunk dict (sheet name + block content)
            
            # breakpoint()
            # block_df = block.dropna(axis=1, how='all')

            chunks.append({
                'sheet': sheet_name,
                'content': block.to_string(index=False, header=False)
            })
    
    return chunks


def vectorize_chunks(chunks, model_name):
    """
    vectorize the chunks
    """
    pass


# def raw_data_parsing(path):
#     """
#     remove NaN values
#     """
#     df = pd.read_excel(path)
#     df = df.dropna()
#     return df

# Example usage:
chunks = chunk_excel_by_scattered_sections("/Users/michael/Desktop/eparse/藍圖.xlsx")
for i, c in enumerate(chunks):
    print(f"--- Chunk {i+1}  (sheet: {c['sheet']}) ---")
    print(c['content'])
    print()