import pandas as pd

# BUG this may not be the best way to do it, since it drops all nan rows, and we need those
# nan rows to represent spacing between blocks
def get_contiguous_blocks(df):
    # NOTE get row indexes that are not null 
    blocks, current_rows = [], []
    for row_idx in range(len(df)):
        if df.iloc[row_idx].notnull().any():
            current_rows.append(row_idx)
        else:
            # NOTE found null, meaning that a complete block is found,
            # store the block and reset the current_rows
            if current_rows:
                block = df.iloc[current_rows].dropna(axis=1, how='all')
                blocks.append(block)
                current_rows = []

    # NOTE process the "last" block (edge case)
    if current_rows:
        block = df.iloc[current_rows].dropna(axis=1, how='all')
        blocks.append(block)
    return blocks

def chunk_excel_scattered(path):
    xls = pd.ExcelFile(path)
    sections = []
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name, header=None)
        blocks = get_contiguous_blocks(df)

        # blocks[0].to_pickle("csv_sample_block_data_after_first_stage.pkl")
        # breakpoint()

        # TODO need to identify section name
        # for i, block in enumerate(blocks):

            #### add new code logic here ####
            # TODO use NaN as boundary to identify section name and then find blocks recursively
            # think of it like a 2-D grid, each dimension needs to store a start and end indexes, from which
            # the stopping condition is when the traversing pointer meets NaN value
            # once the block is identified, extract the block and give it a section name (can be named using an id)
            # then continue to traverse the grid until the end of the sheet

            # breakpoint()

            # text = block.to_string(index=False, header=False)
            # sections.append((sheet_name, section_name, i, text))
    return sections