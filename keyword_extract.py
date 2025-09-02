import sqlite3
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from sqlite_connection import ConnectionPool

"""
extract keywords to analyze and generate queries for RAG
"""


# ---- CONFIG ----
SQLITE_PATH = "/Users/michael/Desktop/eparse/simple-rag/rag_spreadsheet.db"
TOP_N_KEYWORDS = 20
# ----------------

def chinese_tokenizer(text):
    """
    Tokenizer for Chinese using jieba.
    Returns a list of tokens for the given text.
    """
    return list(jieba.cut(text))

# 1. Connect to SQLite
# conn = sqlite3.connect(SQLITE_PATH)
# cursor = conn.cursor()

# 2. Fetch all raw_text data
# cursor.execute("SELECT raw_text FROM sections")
# rows = cursor.fetchall()
# documents = [row[0] for row in rows]

# conn.close()

# 3. Build TF-IDF vectorizer with Chinese tokenizer
# vectorizer = TfidfVectorizer(
#     tokenizer=chinese_tokenizer,
#     stop_words=None  # (Optional) put a list of Chinese stopwords here
# )
# tfidf_matrix = vectorizer.fit_transform(documents)

# # 4. Sum tfidf scores for each term across the entire corpus
# feature_names = vectorizer.get_feature_names_out()
# term_scores = np.asarray(tfidf_matrix.sum(axis=0)).ravel()
# sorted_idx = np.argsort(term_scores)[::-1]

# # 5. Get top N terms
# top_terms = [feature_names[i] for i in sorted_idx[:TOP_N_KEYWORDS]]

# print(f"Top {TOP_N_KEYWORDS} keywords:")
# for t in top_terms:
#     print("-", t)