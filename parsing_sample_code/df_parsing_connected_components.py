import pandas as pd
import numpy as np
from scipy.ndimage import label
import markdown

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

    # PATH = "/Users/michael/Desktop/eparse/simple-rag/藍圖.xlsx"
    PATH = "/Users/michael/Desktop/eparse/simple-rag/sample_data/messy_crm_sales_one_sheet.xlsx"

    sections = parse_df_connected_components(PATH)

    for section in sections[0]:
        html = markdown.markdown(section[3])
        print(html)


    # example output
    # <p>| 7                                  |
    # |:-----------------------------------|
    # | Sales Opportunities (Mixed Schema) |</p>
    # <p>| 7              | 8         | 9             | 10        | 11              | 12       |
    # |:---------------|:----------|:--------------|:----------|:----------------|:---------|
    # | Opportunity ID | Customer  | Stage         | Value ($) | Probability (%) | Owner    |
    # | 101            | Acme Corp | Prospecting   | 50000     | 20              | JDoe     |
    # | 102            | Globex    | Negotiation   | 120000    | 60              | JSmith   |
    # | 103            | Initech   | Closed Won    | 75000     | 100             | PGibbons |
    # | 104            | Umbrella  | Closed Lost   | 30000     | 0               | AWesker  |
    # | 105            | Hooli     | Proposal      | 150000    | nan             | GBelson  |
    # | nan            | Soylent   | Qualification | 45000     | 30              | nan      |</p>
    # <p>| 1                                |
    # |:---------------------------------|
    # | Campaign Performance (Scattered) |</p>
    # <p>| 9                                                                |
    # |:-----------------------------------------------------------------|
    # | Notes from Sales VP (Aug): Focus on ACV &gt; $50k; push multi-year. |
    # | Reminder: GDPR compliance checks before emailing EU leads.       |
    # | Finance: discount approvals must include rationale in ticket.    |
    # | Action items: Demo for Soylent; proposal revision for Hooli.     |</p>
    # <p>| 1                  | 2         | 3     | 4           | 5                                   |
    # |:-------------------|:----------|:------|:------------|:------------------------------------|
    # | Campaign           | Spend ($) | Leads | Conversions | Comments                            |
    # | Email Blast Q3     | 2000      | 25    | 3           | Open rate ~15%. Follow-up.          |
    # | Trade Show - Vegas | 10000     | 100   | 15          | Captured 100+ leads; quality varied |
    # | Google Ads - Brand | 5000      | 45    | 4           | CTR moderate; retargeting planned   |</p>
    # <p>| 1                     |    2 |   3 |   4 | 5                            |
    # |:----------------------|-----:|----:|----:|:-----------------------------|
    # | LinkedIn ABM          | 3000 |  20 |   2 | High-quality leads           |
    # | Webinar: Data Privacy |  nan |  65 |   9 | Reg-heavy audience; long Q&amp;A |</p>
    # <p>| 3                             |
    # |:------------------------------|
    # | Customer Contacts (EU Region) |</p>
    # <p>| 3                | 4      | 5             | 6                   | 7        |
    # |:-----------------|:-------|:--------------|:--------------------|:---------|
    # | Customer         | Region | Contact       | Email               | Phone    |
    # | Umbrella         | EU     | Albert Wesker | wesker@umbrella.com | 555-6789 |
    # | Vehement Capital | EU     | Oliver Queen  | nan                 | 555-7799 |
    # | nan              | EU     | —             | nan                 | nan      |
    # | Globex GmbH      | EU     | Anna Müller   | anna@globex.eu      | nan      |</p>
    # <p>| 9                 |
    # |:------------------|
    # | Reseller Partners |</p>
    # <p>| 7                              |
    # |:-------------------------------|
    # | Sales Opportunities (Fragment) |</p>
    # <p>| 1                            |
    # |:-----------------------------|
    # | Pipeline Summary (Pivot-ish) |</p>

