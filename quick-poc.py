# quick_poc.py
import sqlite3
import pandas as pd
import numpy as np
import faiss

from sqlite_connection import ConnectionPool
from keyword_extract import chinese_tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer

import json

# ---- config ----
EXCEL_PATH = "/Users/michael/Desktop/eparse/simple-rag/藍圖.xlsx"
EMBEDDING_DIM = 1536        # set this to match your embedding model
K_TOP = 3                   # number of retrieval results

# ---- 1. Utility: chunk scattered sections ----
def get_contiguous_blocks(df):
    blocks, current_rows = [], []
    for row_idx in range(len(df)):
        if df.iloc[row_idx].notnull().any():
            current_rows.append(row_idx)
        else:
            if current_rows:
                block = df.iloc[current_rows].dropna(axis=1, how='all')
                blocks.append(block)
                current_rows = []
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

        # TODO need to identify section name
        for i, block in enumerate(blocks):

            #### add new code logic here ####
            # TODO use NaN as boundary to identify section name and then find blocks recursively
            # think of it like a 2-D grid, each dimension needs to store a start and end indexes, from which
            # the stopping condition is when the traversing pointer meets NaN value
            # once the block is identified, extract the block and give it a section name (can be named using an id)
            # then continue to traverse the grid until the end of the sheet

            breakpoint()

            text = block.to_string(index=False, header=False)
            sections.append((sheet_name, section_name, i, text))
    return sections

# ---- 2. Init SQLite and store raw sections ----
def init_and_insert_sections(sections, cursor, conn):
    """
    use connection pool to insert data into sqlite
    """

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sections (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sheet_name TEXT NOT NULL,
        section_name TEXT NOT NULL,
        section_index INTEGER NOT NULL,
        raw_text TEXT NOT NULL
    )""")

    cursor.executemany(
        "INSERT INTO sections (sheet_name, section_name, section_index, raw_text) VALUES (?, ?, ?, ?)",
        sections
    )

    conn.commit()

    cursor.execute("SELECT id, raw_text FROM sections")

    all_rows = cursor.fetchall()

    return all_rows, cursor

# ---- 3. Embed sections (dummy embeddings for now)  ----
def embed_sections(section_rows):
    vectors = []
    ids = []
    for section_id, raw_text in section_rows:
        # Replace this with your real embedding call
        vec = np.random.rand(EMBEDDING_DIM).astype('float32')
        vectors.append(vec)
        ids.append(section_id)
    return ids, np.vstack(vectors)

# ---- 4. Build FAISS index ----
def build_index(vectors):
    index = faiss.IndexFlatIP(EMBEDDING_DIM)
    index.add(vectors)
    return index

# ---- 5. Test query ----
def do_test_query(index, ids, section_rows):
    # Example query_vector (replace w/ real embedding of a query)
    qvec = np.random.rand(EMBEDDING_DIM).astype('float32').reshape(1, -1)

    distances, idxs = index.search(qvec, K_TOP)
    print("\n=== Top results ===")
    for i in idxs[0]:
        section_id = ids[i]
        # find full text for this section
        raw_text = next(text for row_id, text in section_rows if row_id == section_id)
        print(f"[section_id = {section_id}] – preview:\n{raw_text[:200]}...\n")

def extract_keywords(cursor):
    """
    extract keywords from documents
    """

    cursor.execute("SELECT raw_text FROM sections")
    rows = cursor.fetchall()
    documents = [row[0] for row in rows]

    # 3. Build TF-IDF vectorizer with Chinese tokenizer
    vectorizer = TfidfVectorizer(
        tokenizer=chinese_tokenizer,
        stop_words=None  # (Optional) put a list of Chinese stopwords here
    )
    tfidf_matrix = vectorizer.fit_transform(documents)

    # 4. Sum tfidf scores for each term across the entire corpus
    feature_names = vectorizer.get_feature_names_out()
    term_scores = np.asarray(tfidf_matrix.sum(axis=0)).ravel()
    sorted_idx = np.argsort(term_scores)[::-1]

    # 5. Get top N terms
    top_terms = [feature_names[i] for i in sorted_idx[:TOP_N_KEYWORDS]]

    return top_terms, cursor


# ======================
# Main flow
# ======================
if __name__ == "__main__":
    TOP_N_KEYWORDS = 20
    SQLITE_PATH = "/Users/michael/Desktop/eparse/simple-rag/rag_spreadsheet.db"
    print("> Chunking Excel ...")
    chunks = chunk_excel_scattered(EXCEL_PATH)

    print("initializing sqlite connection ...")
    pool = ConnectionPool(SQLITE_PATH)

    with pool.get_connection() as conn:
        cursor = conn.cursor()

    print("inserting sections into sqlite ...")
    rows, cursor = init_and_insert_sections(chunks, cursor, conn)

    print("extracting keywords from sections and save as json ...")
    keywords, cursor = extract_keywords(cursor)
    with open("keywords.json", "w", encoding="utf-8") as f:
        json.dump(keywords, f, ensure_ascii=False)

    print("generating embeddings ...")
    ids, vectors = embed_sections(rows)

    print("building FAISS index ...")
    index = build_index(vectors)

    print("running test query ...")
    # do_test_query(index, ids, rows)