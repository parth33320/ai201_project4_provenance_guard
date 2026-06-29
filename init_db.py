import sqlite3

def init_db(db_path='provenance_guard.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Audit log table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS audit_log (
        content_id TEXT PRIMARY KEY,
        creator_id TEXT NOT NULL,
        text TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        attribution TEXT NOT NULL,
        confidence REAL NOT NULL,
        llm_score REAL,
        stylo_score REAL,
        status TEXT DEFAULT 'classified',
        appeal_reasoning TEXT,
        is_verified INTEGER DEFAULT 0
    )
    ''')

    # Verified creators table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS verified_creators (
        creator_id TEXT PRIMARY KEY,
        verified_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT DEFAULT 'active'
    )
    ''')

    conn.commit()
    conn.close()
    print(f"Database initialized at {db_path}")

if __name__ == "__main__":
    init_db()
