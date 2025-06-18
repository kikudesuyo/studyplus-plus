import sqlite3

DB_NAME = "studyplus-plus.db"

uri = f"file:{DB_NAME}?mode=rwc"

conn = sqlite3.connect(uri, uri=True)


cur = conn.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        studyplus_user_id TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
)

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS battle (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        start_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        end_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
)

cur.execute(
    """    
    CREATE TABLE IF NOT EXISTS result   (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL REFERENCES user(id),
        battle_id INTEGER NOT NULL REFERENCES battle(id),
        place INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
)


conn.commit()
conn.close()
