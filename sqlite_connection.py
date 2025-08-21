import sqlite3
from contextlib import contextmanager

class ConnectionPool:
    def __init__(self, db_path, max_connections=5):
        self.db_path = db_path
        self.max_connections = max_connections
        self.connections = []
        self._initialize_pool()
    
    def _initialize_pool(self):
        for _ in range(self.max_connections):
            conn = sqlite3.connect(self.db_path)
            self.connections.append(conn)
    
    @contextmanager
    def get_connection(self):
        if not self.connections:
            raise Exception("No available connections")
        
        conn = self.connections.pop()
        try:
            yield conn
        finally:
            # Return connection to pool instead of closing
            self.connections.append(conn)
    
    def close_all(self):
        for conn in self.connections:
            conn.close()
        self.connections.clear()

# Usage:
# pool = ConnectionPool("rag_spreadsheet.db")

# with pool.get_connection() as conn:
#     cursor = conn.cursor()
#     cursor.execute("SELECT * FROM sections")
#     results = cursor.fetchall()