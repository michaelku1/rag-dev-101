import sqlite3

# Create (or connect to) the database file
conn = sqlite3.connect("rag_spreadsheet.db")
cursor = conn.cursor()

# sections = raw chunks
cursor.execute("""
CREATE TABLE IF NOT EXISTS sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_name TEXT NOT NULL,
    sheet_name TEXT NOT NULL,
    section_index INTEGER NOT NULL,
    raw_text TEXT NOT NULL,
    processing_status TEXT NOT NULL DEFAULT 'UNPROCESSED',
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
)
""")

# embeddings = derived vectors
cursor.execute("""
CREATE TABLE IF NOT EXISTS embeddings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    section_id INTEGER NOT NULL,
    embedding_vector BLOB NOT NULL,
    model_name TEXT NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(section_id) REFERENCES sections(id)
)
""")

conn.commit()
conn.close()