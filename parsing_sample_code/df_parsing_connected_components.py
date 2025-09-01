import pandas as pd
import numpy as np
from scipy.ndimage import label

"""
finds connected components in an n-dimensional array (e.g like finding pixels that are non-zero on a 2D-grid)
"""


def parse_df_connected_components(path):

    """
    wrapper function to parse the excel file and return a list of sections
    """

    xls = pd.ExcelFile(path)
    sections = []
    for sheet_name in xls.sheet_names:
        df = xls.parse(sheet_name, header=None)
        sections.append(parse_df_connected_components_2d(df, sheet_name))

    return sections

def parse_df_connected_components_2d(df, sheet_name):
    """
    parse the dataframe and return a list of sections
    """

    # store sections in a list of tuples (sheet_name, section_name, i, text) for the defined schema format
    sections = []
    mask = ~df.isna()

    structure = np.array([[1,1,1],
                        [1,1,1],
                        [1,1,1]])

    labeled, num_features = label(mask, structure=structure)

    blocks = []
    for i in range(1, num_features+1):

        # NOTE get the section name, need to find a better way to do this
        # section_name = df.iloc[positions[0][0], positions[0][1]]
        section_name = "section_" + str(i)

        positions = np.argwhere(labeled == i)
        # Ignore blocks touching the edge
        if positions[:,0].min() == 0 or positions[:,0].max() == df.shape[0]-1 \
        or positions[:,1].min() == 0 or positions[:,1].max() == df.shape[1]-1:
            continue
        row_min, col_min = positions.min(axis=0)
        row_max, col_max = positions.max(axis=0)
        block = df.iloc[row_min:row_max+1, col_min:col_max+1]
        block_markdown = block.to_markdown(index=False)
        blocks.append(block_markdown)
        sections.append((sheet_name, section_name, i, block_markdown))

    return sections


    # check results
    # for idx, block in enumerate(blocks):
    #     print(f"Block {idx+1} boundary: rows {block[0]}, cols {block[1]}")
    #     print(df.iloc[block[0][0]:block[0][1]+1, block[1][0]:block[1][1]+1])
    #     print()

if __name__ == "__main__":

    path = "/Users/michael/Desktop/eparse/simple-rag/藍圖.xlsx"
    sections = parse_df_connected_components(path)


