import sqlite3

DB_NAME = "studyplus-plus.db"

uri = f"file:{DB_NAME}?mode=wo"

conn = sqlite3.connect(uri, uri=True)


cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        studyplus_user_id INTEGER NOT NULL UNIQUE,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
)
cur.execute(
    """    
    CREATE TABLE IF NOT EXISTS winner  (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES user(id),
        win_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
)


conn.commit()
conn.close()
