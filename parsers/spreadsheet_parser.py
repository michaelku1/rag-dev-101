from .base_parser import BaseParser
from typing import List, Tuple

import pandas as pd
import numpy as np
from scipy.ndimage import label

class SpreadsheetParser(BaseParser):
    def __init__(self, file_path) -> None:
        super().__init__()

    def parse(self, file_path: str) -> List[List[Tuple[str, ...]]]:
        xls = pd.ExcelFile(file_path)
        sections = []
        for sheet_name in xls.sheet_names:
            df = xls.parse(sheet_name, header=None)
            sections.append(self._parse_data(df, sheet_name))

        return sections
    
    def _parse_data(self, df, sheet_name: pd.DataFrame) -> List[pd.DataFrame]:

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